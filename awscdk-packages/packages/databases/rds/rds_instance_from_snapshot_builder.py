from aws_cdk import aws_rds as rds, aws_ec2 as ec2, Stack, Duration, RemovalPolicy

from packages.builder import Builder


class RdsInstanceFromSnapshotBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__snapshot_identifier = None
        self.__engine = None
        self.__vpc = None
        self.__credentials = None
        self.__instance_type = None
        self.__port = None
        self.__multi_az = None
        self.__auto_minor_version_upgrade = True
        self.__allocated_storage = None
        self.__deletion_protection = True
        self.__publicly_accessible = False
        self.__removal_policy = RemovalPolicy.SNAPSHOT  # (remove the resource, but retain a snapshot of the data)
        self.__creds_rotation_days = 30
        self.__security_groups = None

    def snapshot_identifier(self, snapshot_identifier: str):
        self.__snapshot_identifier = snapshot_identifier

    def engine(self, engine: rds.DatabaseInstanceEngine):
        self.__engine = engine

    def vpc(self, vpc):
        self.__vpc = vpc

    def credentials(self, credentials: str):
        self.__credentials = rds.SnapshotCredentials.from_generated_secret(credentials)

    def instance_type(self, instance_type: ec2.InstanceType):
        self.__instance_type = instance_type

    def port(self, port):
        self.__port = port

    def multi_az(self, multi_az):
        self.__multi_az = multi_az

    def auto_minor_version_upgrade(self, auto_minor_version_upgrade):
        self.__auto_minor_version_upgrade = auto_minor_version_upgrade

    def allocated_storage(self, allocated_storage):
        self.__allocated_storage = allocated_storage

    def deletion_protection(self, deletion_protection):
        self.__deletion_protection = deletion_protection

    def publicly_accessible(self, publicly_accessible):
        self.__publicly_accessible = publicly_accessible

    def removal_policy(self, removal_policy):
        self.__removal_policy = removal_policy

    def creds_rotation_days(self, creds_rotation_days):
        self.__creds_rotation_days = creds_rotation_days

    def security_groups(self, security_groups):
        self.__security_groups = security_groups

    def build(self) -> rds.DatabaseInstance:
        instance = rds.DatabaseInstanceFromSnapshot(self.stack, self.construct_id,
                                                    snapshot_identifier=self.__snapshot_identifier,
                                                    engine=self.__engine,
                                                    vpc=self.__vpc,
                                                    vpc_subnets=ec2.SubnetSelection(
                                                        subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                                                    ),
                                                    credentials=self.__credentials,
                                                    instance_type=self.__instance_type,
                                                    port=self.__port,
                                                    multi_az=self.__multi_az,
                                                    auto_minor_version_upgrade=self.__auto_minor_version_upgrade,
                                                    allocated_storage=self.__allocated_storage,
                                                    deletion_protection=self.__deletion_protection,
                                                    publicly_accessible=self.__publicly_accessible,
                                                    removal_policy=self.__removal_policy,
                                                    security_groups=[self.__security_groups]
                                                    )
        # Add single-user rotation to the RDS instance
        instance.add_rotation_single_user(
            automatically_after=Duration.days(self.__creds_rotation_days)
        )
        return instance
