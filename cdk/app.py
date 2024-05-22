#!/usr/bin/env python3

import aws_cdk as cdk
from cdk.vpc_stack import CdkVpcStack
from cdk.eks_stack import EksStack
from cdk.ssm_stack import SsmStack
from cdk.cr_stack import CRStack


app = cdk.App()
vpc_stack = CdkVpcStack(app, "VPCStack")
ssm_stack = SsmStack(app, "SSMStack")

cr_stack = CRStack(app, "CRStack")
cr_stack.add_dependency(ssm_stack)

eks_stack = EksStack(app, "EKSStack", vpc=vpc_stack.vpc, helm_values=cr_stack.helm_values.get_att_string(attribute_name="helm_values"))
eks_stack.add_dependency(cr_stack)

app.synth()