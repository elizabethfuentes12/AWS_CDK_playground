import json
import pytest

from aws_cdk import core
from s3_to_dynamo.s3_to_dynamo_stack import S3ToDynamoStack


def get_template():
    app = core.App()
    S3ToDynamoStack(app, "s3-to-dynamo")
    return json.dumps(app.synth().get_stack("s3-to-dynamo").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
