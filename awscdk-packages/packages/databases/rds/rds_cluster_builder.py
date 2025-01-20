from aws_cdk import aws_rds as rds, aws_ec2 as ec2, Stack, Duration, RemovalPolicy

from packages.builder import Builder

FIRST_READER_REPLICA = 1


class RdsClusterBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__engine = None
        self.__vpc = None
        self.__credentials = None
        self.__port = None
        self.__deletion_protection = True
        self.__removal_policy = RemovalPolicy.SNAPSHOT  # (remove the resource, but retain a snapshot of the data)
        self.__creds_rotation_days = 30
        self.__security_groups = None
        self.__storage_encrypted = True
        self.__cluster_identifier = None
        self.__readers = []
        self.__serverless_v2_min_capacity = None
        self.__serverless_v2_max_capacity = None

    def engine(self, engine: rds.DatabaseInstanceEngine):
        self.__engine = engine

    def vpc(self, vpc):
        self.__vpc = vpc

    def credentials(self, credentials: str):
        self.__credentials = rds.Credentials.from_generated_secret(credentials)

    def port(self, port):
        self.__port = port

    def deletion_protection(self, deletion_protection):
        self.__deletion_protection = deletion_protection

    def removal_policy(self, removal_policy):
        self.__removal_policy = removal_policy

    def creds_rotation_days(self, creds_rotation_days):
        self.__creds_rotation_days = creds_rotation_days

    def security_groups(self, security_groups):
        self.__security_groups = security_groups

    def storage_encrypted(self, storage_encrypted):
        self.__storage_encrypted = storage_encrypted

    def cluster_identifier(self, cluster_identifier):
        self.__cluster_identifier = cluster_identifier

    def serverless_v2_min_capacity(self, serverless_v2_min_capacity):
        self.__serverless_v2_min_capacity = serverless_v2_min_capacity

    def serverless_v2_max_capacity(self, serverless_v2_max_capacity):
        self.__serverless_v2_max_capacity = serverless_v2_max_capacity

    def readers(self, reader_instances: int):
        """
        Number of required reader instances

        :type reader_instances: positive number
        """
        for instance_idx in range(1, reader_instances + 1):
            is_first_reader = instance_idx == FIRST_READER_REPLICA
            self.__readers.append(rds.ClusterInstance.serverless_v2(f"reader-{instance_idx}",
                                                                    scale_with_writer=is_first_reader,
                                                                    auto_minor_version_upgrade=True,
                                                                    publicly_accessible=False))

    def build(self) -> rds.DatabaseInstance:
        instance = rds.DatabaseCluster(self.stack, self.construct_id,
                                       cluster_identifier=self.__cluster_identifier,
                                       engine=self.__engine,
                                       writer=rds.ClusterInstance.serverless_v2("writer",
                                                                                auto_minor_version_upgrade=True,
                                                                                publicly_accessible=False),
                                       readers=self.__readers,
                                       vpc=self.__vpc,
                                       vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
                                       serverless_v2_min_capacity=self.__serverless_v2_min_capacity,
                                       serverless_v2_max_capacity=self.__serverless_v2_max_capacity,
                                       credentials=self.__credentials,
                                       port=self.__port,
                                       deletion_protection=self.__deletion_protection,
                                       removal_policy=self.__removal_policy,
                                       security_groups=[self.__security_groups],
                                       storage_encrypted=self.__storage_encrypted)

        # Add single-user rotation to the RDS instance
        instance.add_rotation_single_user(automatically_after=Duration.days(self.__creds_rotation_days))

        return instance
