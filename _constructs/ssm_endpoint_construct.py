from constructs import Construct
from aws_cdk import aws_ec2
from aws_cdk import Tags


class SsmEndpointConstruct(Construct):
    def __init__(self,
                 scope: Construct,
                 id: str,
                 vpc: aws_ec2.CfnVPC,
                 region: str,
                 subnet_private_3a: aws_ec2.CfnSubnet,
                 route_table: aws_ec2.CfnRouteTable,
                 ) -> None:
        super().__init__(scope, id)

        # ---------------------------------------
        # Security Group
        # ---------------------------------------
        ssm_endpoint_ingress = aws_ec2.CfnSecurityGroup.IngressProperty(
            ip_protocol='tcp',
            cidr_ip='0.0.0.0/0',
            from_port=443,
            to_port=443,
            description='SSM endpoint SG'
        )
        ssm_endpoint_sg = aws_ec2.CfnSecurityGroup(
            scope=self,
            id='SsmEndpointSecurityGroup',
            vpc_id=vpc.ref,
            group_description='Security Group for SSM Endpoint',
            group_name='ssm-endpoint-sg',
            security_group_ingress=[ssm_endpoint_ingress],
        )
        Tags.of(ssm_endpoint_sg).add('Name', 'ssm-endpoint-sg')

        # ---------------------------------------
        # SSM Private Link
        # ---------------------------------------
        ssm_endpoint = aws_ec2.CfnVPCEndpoint(
            self,
            id='SsmEndpoint',
            vpc_endpoint_type='Interface',
            service_name=f'com.amazonaws.{region}.ssm',
            private_dns_enabled=True,
            vpc_id=vpc.ref,
            subnet_ids=[subnet_private_3a.ref],
            security_group_ids=[ssm_endpoint_sg.ref]
        )
        Tags.of(ssm_endpoint).add('Name', 'ssm-endpoint')

        ssm_message_endpoint = aws_ec2.CfnVPCEndpoint(
            self,
            id='SsmMessageEndpoint',
            vpc_endpoint_type='Interface',
            service_name=f'com.amazonaws.{region}.ssmmessages',
            private_dns_enabled=True,
            vpc_id=vpc.ref,
            subnet_ids=[subnet_private_3a.ref],
            security_group_ids=[ssm_endpoint_sg.ref]
        )
        Tags.of(ssm_message_endpoint).add('Name', 'ssm-message-endpoint')

        ec2_endpoint = aws_ec2.CfnVPCEndpoint(
            self,
            id='Ec2Endpoint',
            vpc_endpoint_type='Interface',
            service_name=f'com.amazonaws.{region}.ec2',
            private_dns_enabled=True,
            vpc_id=vpc.ref,
            subnet_ids=[subnet_private_3a.ref],
            security_group_ids=[ssm_endpoint_sg.ref]
        )
        Tags.of(ec2_endpoint).add('Name', 'ec2-endpoint')

        ec2_message_endpoint = aws_ec2.CfnVPCEndpoint(
            self,
            id='Ec2MessageEndpoint',
            vpc_endpoint_type='Interface',
            service_name=f'com.amazonaws.{region}.ec2messages',
            private_dns_enabled=True,
            vpc_id=vpc.ref,
            subnet_ids=[subnet_private_3a.ref],
            security_group_ids=[ssm_endpoint_sg.ref]
        )
        Tags.of(ec2_message_endpoint).add('Name', 'ec2-message-endpoint')

        s3_endpoint = aws_ec2.CfnVPCEndpoint(
            self,
            id='S3Endpoint',
            vpc_endpoint_type='Gateway',
            service_name=f'com.amazonaws.{region}.s3',
            vpc_id=vpc.ref,
            route_table_ids=[route_table.ref]
        )
        Tags.of(s3_endpoint).add('Name', 's3-endpoint')
