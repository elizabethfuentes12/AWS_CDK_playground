#!/usr/bin/env python3

from aws_cdk import core

from s3_to_dynamo.s3_to_dynamo_stack import S3ToDynamoStack


app = core.App()
S3ToDynamoStack(app, "s3-to-dynamo", env={'region': 'us-east-1'})

app.synth()
