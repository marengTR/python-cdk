from aws_cdk import aws_ssm as ssm
from aws_cdk import CfnOutput, Stack
from constructs import Construct

class SsmStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ssm.StringParameter(
            self,
            "SSMParameter",
            parameter_name="/platform/account/env",
            string_value="development"
        )
