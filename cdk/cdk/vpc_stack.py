from aws_cdk import CfnOutput, Stack
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

VPC_CIDR_BLOCK="10.200.0.0/20"
CIDR_MASK=24

class CdkVpcStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs=2,
                           vpc_name="Demo",
                           ip_addresses = ec2.IpAddresses.cidr(VPC_CIDR_BLOCK), #cidr="10.200.0.0/20",
                           # configuration will create 2 groups in 2 AZs = 4 subnets.
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name="Public",
                            #    enable_dns_support = True,
                               cidr_mask=CIDR_MASK
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                               name="Private",
                            #    enable_dns_support = True,
                               cidr_mask=CIDR_MASK
                           )
                           ],
                           # nat_gateway_provider=ec2.NatProvider.gateway(),
                           nat_gateways=1,
                           )
        CfnOutput(self, "Output",
                   value=self.vpc.vpc_id)