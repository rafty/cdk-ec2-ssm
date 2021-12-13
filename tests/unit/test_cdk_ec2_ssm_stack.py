import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_ec2_ssm.cdk_ec2_ssm_stack import CdkEc2SsmStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_ec2_ssm/cdk_ec2_ssm_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkEc2SsmStack(app, "cdk-ec2-ssm")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
