from aws_cdk import core

#from app.s3_bucket_stack import S3BucketStack

from app.s3_bucket_stack import S3BucketStack

class AppStack:

    def __init__(self):
        self.app = core.App()

    def build(self) -> core.App:

        primary_stack = S3BucketStack(
            self.app,
            "primary-stack",
            env={'region':'us-east-1'}
        )

        secondary_stack = S3BucketStack(
            self.app,
            "secondary-stack",
            env={'region':'us-west-2'}
        )

        return self.app
