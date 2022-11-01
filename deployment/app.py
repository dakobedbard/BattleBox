#!/usr/bin/env python3
import os

import aws_cdk as cdk

from battlebox_deployment_stack.battlebox_deployment_stack import BattleBoxDeploymentStack

account = os.getenv("AWS_ACCOUNT")
region = "us-west-2"
env = cdk.Environment()
if account and region:
    env = cdk.Environment(account=account, region=region)

app = cdk.App()
BattleBoxDeploymentStack(app, "BattleBoxDeploymentStack", env=env)

app.synth()
