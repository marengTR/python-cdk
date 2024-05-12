# from aws_cdk import core
# from aws_cdk import aws_eks as eks
# from aws_cdk import aws_ec2 as ec2
# from aws_cdk import aws_iam as iam

# class EksStack(core.Stack):
#     def __init__(self, scope: core.Construct, id: str, vpc, **kwargs):
#         super().__init__(scope, id, **kwargs)

#         # VPC is passed to the stack from another stack
#         self.vpc = vpc


#         # Creating the EKS cluster
#         self.cluster = eks.Cluster(self, "Demo",
#             vpc=self.vpc,
#             version=eks.KubernetesVersion.V1_29,  # 1.29 Kubernetes version
#             default_capacity=0  # No default capacity; we will add node groups manually
#         )

#         # Define the IAM role for the node group
#         eks_role = iam.Role(self, "eksadmin", assumed_by=iam.ServicePrincipal(service='ec2.amazonaws.com'),
#                             role_name='eks-cluster-role', managed_policies=
#                             [iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name='AdministratorAccess')])
#         eks_instance_profile = iam.CfnInstanceProfile(self, 'instanceprofile',
#                                                       roles=[eks_role.role_name],
#                                                       instance_profile_name='eks-cluster-role')

#         # Adding an Auto Scaling group as a node group
#         self.nodegroup = self.cluster.add_auto_scaling_group_capacity("AutoScalingNodeGroup",
#             instance_types=[ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.LARGE),
#                     ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.LARGE),
#                     ec2.InstanceType.of(ec2.InstanceClass.C5, ec2.InstanceSize.LARGE),
#                     ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
#                     ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.MEDIUM),
#                     ec2.InstanceType.of(ec2.InstanceClass.C5, ec2.InstanceSize.MEDIUM)],
#             min_capacity=1,
#             max_capacity=3,
#             disk_size=20,
#             subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
#             role=self.nodegroup_role
#         )

# # Assuming you are setting up the VPC in another stack, you would typically pass it like this:
# # vpc_stack = VPCStack(app, "VPCStack")
# # eks_stack = EksClusterStack(app, "EksClusterStack", vpc=vpc_stack.vpc)
