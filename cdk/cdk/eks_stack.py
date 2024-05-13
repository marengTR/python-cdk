from aws_cdk import CfnOutput, Stack
from constructs import Construct
from aws_cdk import aws_eks as eks
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk.lambda_layer_kubectl_v29 import KubectlV29Layer

class EksStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc, **kwargs):
        super().__init__(scope, id, **kwargs)

        # VPC is passed to the stack from another stack
        self.vpc = vpc

        # Creating the EKS cluster
        self.cluster = eks.Cluster(self, "Demo",
            vpc=self.vpc,
            vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)],
            version=eks.KubernetesVersion.V1_29,  # 1.29 Kubernetes version
            endpoint_access=eks.EndpointAccess.PUBLIC, # No VPN to connect internally
            kubectl_layer=KubectlV29Layer(self, "kubectl")
        )
        
        existing_user = iam.User.from_user_name(self, "ExistingUser", "Etem")
        self.cluster.aws_auth.add_user_mapping(existing_user, groups=["system:masters"])
        
        self.cluster.add_auto_scaling_group_capacity("AutoScalingGroup",
            instance_type=ec2.InstanceType("t2.medium"),
            min_capacity=5,
            # max_capacity=3,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
        )