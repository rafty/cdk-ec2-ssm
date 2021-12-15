from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_ec2
from _constructs.vpc_construct import VpcConstruct


class VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_construct = VpcConstruct(self, 'VpcConstruct')
        self._vpc = vpc_construct.vpc
        self._subnet_private_1a = vpc_construct.subnet_private_1a
        self._route_table = vpc_construct.route_table

    @property
    def vpc(self) -> aws_ec2.CfnVPC:
        return self._vpc

    @property
    def subnet_private_1a(self) -> aws_ec2.CfnSubnet:
        return self._subnet_private_1a

    @property
    def route_table(self) -> aws_ec2.CfnRouteTable:
        return self._route_table
