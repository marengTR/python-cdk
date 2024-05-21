#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.vpc_stack import CdkVpcStack
from cdk.eks_stack import EksStack
from cdk.ssm_stack import SsmStack
from cdk.lambda_stack import LambdaStack
# from cdk.cr_stack import CRStack1


app = cdk.App()
vpc_stack = CdkVpcStack(app, "VPCStack")
ssm_stack = SsmStack(app, "SSMStack")
lambda_stack = LambdaStack(app, "LambdaStack")

# print(lambda_stack.lambda_func.function_arn)

# cr_stack = CRStack1(app, "CRStack1", lambda_func_arn=lambda_stack.lambda_func.function_arn)
# cr_stack.add_dependency(lambda_stack)
#print out the helm_values_output to console first
print("Hey you are here, and helm_values: ") 
#print(cr_stack.helm_values.get_att_string(attribute_name="helm_values"))
print(vpc_stack.vpc)

eks_stack = EksStack(app, "EKSStack", vpc=vpc_stack.vpc, helm_values=lambda_stack.helm_values.get_att_string(attribute_name="helm_values"))
eks_stack.add_dependency(lambda_stack)
app.synth()