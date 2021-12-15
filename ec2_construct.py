from constructs import Construct
from aws_cdk import aws_ec2
from aws_cdk import aws_iam
from aws_cdk import Tags


class Ec2InstanceConstruct(Construct):
    def __init__(self,
                 scope: Construct,
                 id: str,
                 vpc: aws_ec2.Vpc,
                 iam_role: aws_iam.Role
                 ) -> None:
        super().__init__(scope, id)

        # ---------------------------------------
        # Security Group
        # ---------------------------------------
        my_security_group = aws_ec2.SecurityGroup(
            self,
            'MySecurityGroup',
            security_group_name='my-sg',
            vpc=vpc,
            description='Allow ssh access to ec2 instances from anywhere',
            allow_all_outbound=True
        )
        my_security_group.add_ingress_rule(
            peer=aws_ec2.Peer.any_ipv4(),
            connection=aws_ec2.Port.tcp(22),
            description='allow public ssh access'
        )
        my_security_group.add_ingress_rule(
            peer=aws_ec2.Peer.any_ipv4(),
            connection=aws_ec2.Port.tcp(80),
            description='allow HTTP traffic from anywhere'
        )
        # my_security_group.add_ingress_rule(
        #     peer=aws_ec2.Peer.any_ipv4(),
        #     connection=aws_ec2.Port.tcp(443),
        #     description='allow HTTPS traffic from anywhere'
        # )

        # ---------------------------------------
        # Image
        # ---------------------------------------
        aws_ami = aws_ec2.AmazonLinuxImage(
            generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            cpu_type=aws_ec2.AmazonLinuxCpuType.X86_64
        )

        # ---------------------------------------
        # EC2 Instance
        # ---------------------------------------
        instance_type = aws_ec2.InstanceType('t3.micro')

        vpc_public_subnets = aws_ec2.SubnetSelection(
            subnets=vpc.select_subnets(subnet_type=aws_ec2.SubnetType.PUBLIC).subnets
        )

        self._ec2_instance = aws_ec2.Instance(
            self,
            'EC2Instance',
            instance_name='SsmTest',
            vpc=vpc,
            vpc_subnets=vpc_public_subnets,  # Default: - Private subnets
            instance_type=instance_type,
            machine_image=aws_ami,
            security_group=my_security_group,
            role=iam_role
        )
        Tags.of(self._ec2_instance).add('my_association', 'true')

    @property
    def instance(self):
        return self._ec2_instance

