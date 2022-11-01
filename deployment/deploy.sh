

export AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)

cdk synth

cdk deploy --require-approval-never