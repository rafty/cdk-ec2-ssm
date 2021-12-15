from constructs import Construct
from aws_cdk import aws_ec2
from aws_cdk import Tags
from aws_cdk import Fn


class VpcConstruct(Construct):
    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)

        # ---------------------------------------
        # vpc
        # ---------------------------------------
        self._vpc = aws_ec2.CfnVPC(
            scope=self,
            id='Vpc',
            cidr_block='10.10.0.0/16',
            enable_dns_hostnames=True,
            enable_dns_support=True,
        )
        Tags.of(self._vpc).add('Name', 'dev-vpc')

        # ---------------------------------------
        # private subnet with vpc endpoint
        # ---------------------------------------
        azs = Fn.get_azs()
        self._subnet_private_1a = aws_ec2.CfnSubnet(
            self, 'SubnetPrivate1a',
            cidr_block='10.10.21.0/24',
            vpc_id=self._vpc.ref,
            # availability_zone='ap-northeast-1a',
            availability_zone=Fn.select(0, azs)  # ap-northeast-1a
        )
        Tags.of(self._subnet_private_1a).add('Name', 'dev-subnet-app-1a')

        # ---------------------------------------
        # Route Table
        # S3 endpointにはroute_tableが必要
        # ---------------------------------------
        self._route_table = aws_ec2.CfnRouteTable(
            self,
            id='RouteTableForS3Endpoint',
            vpc_id=self._vpc.ref
        )
        aws_ec2.CfnSubnetRouteTableAssociation(
            self,
            id='S3EndpointRouteTableAssociation',
            route_table_id=self._route_table.ref,
            subnet_id=self._subnet_private_1a.ref
        )
        Tags.of(self._route_table).add('Name', 's3-endpoint-route-table')  # route table名になる。

    @property
    def vpc(self) -> aws_ec2.CfnVPC:
        return self._vpc

    @property
    def subnet_private_1a(self) -> aws_ec2.CfnSubnet:
        return self._subnet_private_1a

    @property
    def route_table(self) -> aws_ec2.CfnRouteTable:
        return self._route_table
