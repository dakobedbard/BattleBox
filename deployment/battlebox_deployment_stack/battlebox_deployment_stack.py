import os
import shutil

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb

)

from aws_cdk import (
    aws_lambda,
)
from constructs import Construct
from battlebox_deployment_stack.python_layer_version import BuildPyLayerAsset


class BattleBoxDeploymentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc.from_lookup(self, id="VPC", is_default=True)
        self.lambda_role = iam.Role(
            self,
            f"lambda-role",
            role_name="BattleBoxLambdaRole",
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com')
        )
        self.layer = self._create_battlebox_logic_layer()
        # create a Lambda layer with two custom python modules


        # self._create_battlebox_lambda_logic_layer()
        self._create_lambdas()
        self._create_dynamo_tables()

    def _create_battlebox_logic_layer(self):
        # create a Lambda layer with two custom python modules
        module_layer_asset = BuildPyLayerAsset.from_modules(self,
                                                            'ModuleLayerAsset',
                                                            local_module_dirs=['../battlebox_lib'],
                                                            py_runtime=aws_lambda.Runtime.PYTHON_3_8,
                                                            )
        layer = aws_lambda.LayerVersion(
            self,
            id='ModuleLayer',
            code=aws_lambda.Code.from_bucket(module_layer_asset.asset_bucket, module_layer_asset.asset_key),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8],
            description='custom python modules lib1, lib2'
        )
        return layer

    def _create_lambdas(self):
        current_dir = os.path.dirname(os.getcwd())
        matches_lambda = _lambda.Function(
            self,
            "matches_lambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset(f"{current_dir}/lambdas/battlebox_matches"),
            handler="handler.lambda_handler",
            role=self.lambda_role,
            allow_public_subnet=True,
            layers=[self.layer]
            # layers=[self.battlebox_logic_layer]
        )

        matches_lambda.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[""
                     "lambda:InvokeFunction",
                     "dynamodb:*"
                     ],
            resources=["*"]
        ))

        # CfnOutput(self, "lambdaurl", value=lambda_url.url)

    def _create_dynamo_tables(self):
        dynamodb.Table(
            self,
            f"MatchesTable",
            table_name="BattleBoxMatch",
            partition_key=dynamodb.Attribute(
                name="match_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
