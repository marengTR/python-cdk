from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    custom_resources as cr,
    aws_ssm as ssm,
    CustomResource,
    CfnOutput,
    RemovalPolicy
)

from constructs import Construct
from os import path
 
class CRStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Define the Lambda function
        self.lambda_func = _lambda.Function(
            self, "HelmValuesFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="helm_values.handler",
            code=_lambda.Code.from_asset(path.join(path.dirname(__file__), "./scripts")),
            environment={
                "PARAMETER_NAME": "/platform/account/env"
            }
        )

        # Grant the Lambda function read access to the SSM parameter
        self.lambda_func.add_to_role_policy(iam.PolicyStatement(
            actions=["ssm:GetParameter"],
            resources=[ssm.StringParameter.from_string_parameter_name(
                self, "Param", "/platform/account/env").parameter_arn]
        ))

        # Grant the Lambda function permissions to write to CloudWatch Logs
        self.lambda_func.add_to_role_policy(iam.PolicyStatement(
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
            resources=["*"]
        ))

        # Grant the Lambda function permissions to send responses to CloudFormation
        self.lambda_func.add_to_role_policy(iam.PolicyStatement(
            actions=["cloudformation:DescribeStacks"],
            resources=["*"]
        ))

        # Define the Custom Resource provider
        res_provider = cr.Provider(
            self,'crProvider',
            on_event_handler= self.lambda_func
        )
        self.helm_values = CustomResource(self, 'CustomResource', service_token=res_provider.service_token)
        # apply removal policy to the custom resource
        self.helm_values.apply_removal_policy(RemovalPolicy.DESTROY)

        # Output the Lambda function ARN to be used in the CustomResource in CRStack as service token
        CfnOutput(self, "LambdaFunctionArn", value=self.lambda_func.function_arn)
        CfnOutput(self, "HelmValues", value=self.helm_values.get_att_string("helm_values"))

        #TODO: Trigger Lambda function for each deployment.