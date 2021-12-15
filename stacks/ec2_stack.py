from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_ec2
from _constructs.iam_construct import IamConstruct
from _constructs.ec2_construct import Ec2InstanceConstruct
from _constructs.ssm_endpoint_construct import SsmEndpointConstruct


class Ec2Stack(Stack):
    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 vpc: aws_ec2.Vpc,
                 private_subnet_1a: aws_ec2.CfnSubnet,
                 route_table: aws_ec2.CfnRouteTable,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        _env = kwargs.get('env')

        iam_construct = IamConstruct(self, 'SSMIamRoleConstruct')

        instance_construct = Ec2InstanceConstruct(
            self, 'InstanceConstruct',
            vpc=vpc,
            subnet=private_subnet_1a,
            iam_role=iam_construct.iam_role
        )

        SsmEndpointConstruct(
            self, 'SsmEndpointConstruct',
            vpc=vpc,
            region=_env.region,
            subnet_private_3a=private_subnet_1a,
            route_table=route_table
        )
