#!/usr/bin/env python3
import os
import aws_cdk as cdk
from stacks.vpc_stack import VpcStack
from stacks.ec2_stack import Ec2Stack

env = cdk.Environment(
    account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
    region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"]),
)

app = cdk.App()

vpc_stack = VpcStack(app, "CdkEc2SsmStack", env=env)

ec2_stack = Ec2Stack(
    app,
    'Ec2Stack',
    vpc=vpc_stack.vpc,
    private_subnet_1a=vpc_stack.subnet_private_1a,
    route_table=vpc_stack.route_table,
    env=env)

ec2_stack.add_dependency(vpc_stack)

app.synth()
