#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.vpc_stack import CdkVpcStack
from cdk.eks_stack import EksStack
# from cdk.ssm_stack import SsmStack


app = cdk.App()
vpc_stack = CdkVpcStack(app, "VPCStack")
eks_stack = EksStack(app, "EKSStack", vpc=vpc_stack.vpc)
# ssm_stack = SsmStack(app, "SSMStack")

app.synth()