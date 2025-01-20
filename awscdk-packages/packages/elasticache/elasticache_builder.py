from aws_cdk import aws_elasticache as elasticache, aws_ec2 as ec2, Stack

from packages.builder import Builder
from packages.utils.vpc_utils import VpcUtils


class ClusterMode:
    ENABLED = "enabled"
    DISABLED = "disabled"


class SubnetGroup(Builder):

    def __init__(self, construct_id: str, stack: Stack, vpc: ec2.Vpc):
        super().__init__(construct_id, stack)
        self.__description = None
        self.__vpc = vpc

    def description(self, description):
        self.__description = description

    def build(self) -> elasticache.CfnSubnetGroup:
        return elasticache.CfnSubnetGroup(
            scope=self.stack, id=self.construct_id,
            subnet_ids=VpcUtils.get_private_subnets(self.__vpc),
            description=self.__description
        )


class ElasticacheBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__replication_group_description = None
        self.__cluster_mode = None
        self.__engine_version = None
        self.__engine = None
        self.__cache_node_type = None
        self.__num_cache_clusters = None
        self.__cache_subnet_group_name = None
        self.__cache_security_group_names = None
        self.__multi_az_enabled = False
        self.__security_group_ids = None
        self.__replication_group_id = None
        self.__global_replication_group_id = None

    def replication_group_description(self, replication_group_description):
        self.__replication_group_description = replication_group_description

    def cluster_mode(self, cluster_mode: ClusterMode):
        self.__cluster_mode = cluster_mode

    def engine_version(self, engine_version):
        self.__engine_version = engine_version

    def engine(self, engine):
        self.__engine = engine

    def cache_node_type(self, cache_node_type):
        self.__cache_node_type = cache_node_type

    def num_cache_clusters(self, num_cache_clusters):
        self.__num_cache_clusters = num_cache_clusters

    def cache_subnet_group_name(self, cache_subnet_group_name):
        self.__cache_subnet_group_name = cache_subnet_group_name

    def cache_security_group_names(self, cache_security_group_names: []):
        self.__cache_security_group_names = cache_security_group_names

    def multi_az_enabled(self, multi_az_enabled: bool):
        self.__multi_az_enabled = multi_az_enabled

    def security_group_ids(self, security_group_ids: []):
        self.__security_group_ids = security_group_ids

    def replication_group_id(self, replication_group_id: str):
        self.__replication_group_id = replication_group_id

    def global_replication_group_id(self, global_replication_group_id: str):
        self.__global_replication_group_id = global_replication_group_id

    def build(self) -> elasticache.CfnReplicationGroup:
        redis_cluster = elasticache.CfnReplicationGroup(self.stack, self.construct_id,
                                                        replication_group_description=self.__replication_group_description,
                                                        multi_az_enabled=self.__multi_az_enabled,
                                                        transit_encryption_enabled=False,
                                                        at_rest_encryption_enabled=True,
                                                        cluster_mode=self.__cluster_mode,
                                                        engine_version=self.__engine_version,
                                                        engine=self.__engine,
                                                        cache_node_type=self.__cache_node_type,
                                                        num_cache_clusters=self.__num_cache_clusters,
                                                        cache_subnet_group_name=self.__cache_subnet_group_name,
                                                        cache_security_group_names=self.__cache_security_group_names,
                                                        security_group_ids=self.__security_group_ids,
                                                        replication_group_id=self.__replication_group_id,
                                                        global_replication_group_id=self.__global_replication_group_id)
        return redis_cluster
