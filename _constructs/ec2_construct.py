from constructs import Construct
from aws_cdk import aws_ec2
from aws_cdk import aws_iam
from aws_cdk import Tags


class Ec2InstanceConstruct(Construct):
    def __init__(self,
                 scope: Construct,
                 id: str,
                 vpc: aws_ec2.Vpc,
                 subnet: aws_ec2.CfnSubnet,
                 iam_role: aws_iam.Role
                 ) -> None:
        super().__init__(scope, id)

        # # ------------------------------------------
        # # SSM Iam Role
        # # ------------------------------------------
        # iam_role = aws_iam.Role(
        #     self, 'SsmTestIamRole',
        #     role_name='SsmTestIamRole',
        #     assumed_by=aws_iam.ServicePrincipal('ec2.amazonaws.com'),
        #     description='Instance Role for SSM access',
        #     managed_policies=[
        #         aws_iam.ManagedPolicy.from_aws_managed_policy_name(
        #             'AmazonSSMManagedInstanceCore'),
        #         aws_iam.ManagedPolicy.from_aws_managed_policy_name(
        #             'CloudWatchAgentServerPolicy')
        #     ]
        # )

        instance_profile = aws_iam.CfnInstanceProfile(
            self, 'TestEc2InstanceProfile',
            roles=[iam_role.role_name],
            instance_profile_name='SsmTestProfile'
        )

        # ---------------------------------------
        # Image
        # ---------------------------------------
        image = aws_ec2.AmazonLinuxImage(
            generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            cpu_type=aws_ec2.AmazonLinuxCpuType.X86_64
        )
        # ---------------------------------------
        # Security Group
        # EC2 Instance 通信要件がないためingress_ruleは何もなし
        # ---------------------------------------
        ssm_test_sg = aws_ec2.CfnSecurityGroup(
            scope=self,
            id='SsmTestSecurityGroup',
            vpc_id=vpc.ref,
            group_description='Allow ssh access to ec2 instances from anywhere',
            group_name='ssm-test-sg',
            security_group_ingress=[],
        )

        # my_security_group = aws_ec2.SecurityGroup(
        #     self,
        #     'MySecurityGroup',
        #     security_group_name='my-sg',
        #     vpc=vpc,
        #     description='Allow ssh access to ec2 instances from anywhere',
        #     allow_all_outbound=True
        # )
        # my_security_group.add_ingress_rule(
        #     peer=aws_ec2.Peer.any_ipv4(),
        #     connection=aws_ec2.Port.tcp(22),
        #     description='allow public ssh access'
        # )
        # my_security_group.add_ingress_rule(
        #     peer=aws_ec2.Peer.any_ipv4(),
        #     connection=aws_ec2.Port.tcp(80),
        #     description='allow HTTP traffic from anywhere'
        # )
        # my_security_group.add_ingress_rule(
        #     peer=aws_ec2.Peer.any_ipv4(),
        #     connection=aws_ec2.Port.tcp(443),
        #     description='allow HTTPS traffic from anywhere'
        # )

        # ------------------------------------------
        # EC2 Instance
        #
        # ------------------------------------------
        self._instance = aws_ec2.CfnInstance(
            self,
            'SsmTestPrivate1a',
            # availability_zone='ap-northeast-1a',
            iam_instance_profile=instance_profile.ref,
            image_id=image.get_image(self).image_id,
            instance_type='t3.micro',
            security_group_ids=[
                ssm_test_sg.ref
            ],
            subnet_id=subnet.ref
        )
        Tags.of(self._instance).add('Name', 'ssm-test-instance-1a')

    @property
    def instance(self):
        return self._instance

