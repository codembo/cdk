from aws_cdk import Stack
from constructs import Construct
from packages.s3.s3_builder import S3Builder

from config import env_config


class S3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        kwargs["description"] = "This stack creates an S3 bucket for IP360."
        super().__init__(scope, construct_id, **kwargs)

        self.__create_s3()

    def __create_s3(self):
        bucket_builder = S3Builder("IP360Bucket", self)
        bucket_builder.bucket_name(env_config.IP360_BUCKET)
        bucket_builder = bucket_builder.build()
        return bucket_builder
