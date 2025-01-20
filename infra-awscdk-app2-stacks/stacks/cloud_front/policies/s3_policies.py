from aws_cdk import aws_iam as iam
from packages.iam.policy_statement_builder import PolicyStatementBuilder

from config import env_config


def create_cf_read_only_policy(s3_bucket, distribution_id):
    cf_read_only_policy_builder = PolicyStatementBuilder("CloudFrontReadOnly")
    cf_read_only_policy_builder.principals = [iam.ServicePrincipal("cloudfront.amazonaws.com")]
    cf_read_only_policy_builder.actions = ["s3:GetObject"]
    cf_read_only_policy_builder.effect = iam.Effect.ALLOW
    cf_read_only_policy_builder.resources = [s3_bucket.arn_for_objects(key_pattern="*")]
    cf_read_only_policy_builder.conditions = {"StringEquals": {
        "AWS:SourceArn": f"arn:aws:cloudfront::{env_config.AWS_DEFAULT_ACCOUNT}:distribution/{distribution_id}"}}
    return cf_read_only_policy_builder.build()
