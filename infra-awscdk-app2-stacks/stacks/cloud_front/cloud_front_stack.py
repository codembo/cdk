from aws_cdk import Stack, aws_cloudfront as cf, aws_cloudfront_origins as origins, aws_certificatemanager as acm
from constructs import Construct
from packages.cloud_front.cloud_front_builder import CloudFrontBuilder
from packages.s3.s3_builder import S3Builder

from config import env_config
from stacks.cloud_front.policies.s3_policies import create_cf_read_only_policy

INDEX_DOC = "/index.html"


class CloudFrontStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        web_app_bucket = self.__create_web_app_bucket()
        distribution = self.__create_distribution(web_app_bucket)
        self.__create_web_app_bucket_policies(web_app_bucket, distribution)

    def __create_web_app_bucket(self):
        bucket_builder = S3Builder("WebAppBucket", self)
        bucket_builder.bucket_name(env_config.WEB_APP_BUCKET)
        bucket_builder = bucket_builder.build()
        return bucket_builder

    def __create_distribution(self, s3_bucket) -> cf.Distribution:
        cloud_front_builder = CloudFrontBuilder("WebAppDist", self)
        cloud_front_builder.certificate(self.__create_certificate_from_arn())
        cloud_front_builder.domain_names(env_config.WEB_APP_DOMAIN_NAMES)
        cloud_front_builder.error_responses(self.__error_responses())
        cloud_front_builder.default_behavior(self.__create_default_behavior(s3_bucket))
        cloud_front_builder.create_origin_access_control(True)
        return cloud_front_builder.build()

    def __create_certificate_from_arn(self):
        return acm.Certificate.from_certificate_arn(self, "Certificate",
                                                    env_config.WEB_APP_CERT)

    @staticmethod
    def __create_default_behavior(s3_bucket):
        return cf.BehaviorOptions(
            origin=origins.S3Origin(s3_bucket, origin_id="WebApp"),
            compress=True,
            allowed_methods=cf.AllowedMethods.ALLOW_GET_HEAD,
            cache_policy=cf.CachePolicy.CACHING_OPTIMIZED,
            viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS)

    @staticmethod
    def __error_responses():
        return [cf.ErrorResponse(http_status=403,
                                 response_http_status=200,
                                 response_page_path=INDEX_DOC),
                cf.ErrorResponse(http_status=404,
                                 response_http_status=200,
                                 response_page_path=INDEX_DOC)]

    @staticmethod
    def __create_web_app_bucket_policies(web_app_bucket, distribution):
        web_app_bucket.add_to_resource_policy(create_cf_read_only_policy(web_app_bucket,
                                                                         distribution.distribution_id))
