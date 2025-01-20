from aws_cdk import aws_dynamodb as dynamodb, Stack

from packages.builder import Builder


class DynamodbBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__table_name = None
        self.__partition_key = None
        self.__sort_key = None
        self.__table_class = dynamodb.TableClass.STANDARD
        self.__point_in_time_recovery = True
        self.__deletion_protection = True
        self.__global_secondary_indexes = []
        self.__local_secondary_indexes = []

    def table_name(self, table_name):
        self.__table_name = table_name
        return self

    def partition_key(self, partition_key):
        self.__partition_key = partition_key
        return self

    def sort_key(self, sort_key):
        self.__sort_key = sort_key
        return self

    def table_class(self, table_class):
        self.__table_class = table_class
        return self

    def point_in_time_recovery(self, point_in_time_recovery):
        self.__point_in_time_recovery = point_in_time_recovery
        return self

    def deletion_protection(self, deletion_protection):
        self.__deletion_protection = deletion_protection
        return self

    def add_global_secondary_index(self, index_name, partition_key_name, sort_key_name,
                                   partition_key_type=dynamodb.AttributeType.STRING,
                                   sort_key_type=dynamodb.AttributeType.STRING,
                                   projection_type=dynamodb.ProjectionType.ALL):
        index = dynamodb.GlobalSecondaryIndexPropsV2(index_name=index_name,
                                                     projection_type=projection_type,
                                                     partition_key=dynamodb.Attribute(name=partition_key_name,
                                                                                      type=partition_key_type),
                                                     sort_key=dynamodb.Attribute(name=sort_key_name,
                                                                                 type=sort_key_type))
        self.__global_secondary_indexes.append(index)

    def add_local_secondary_index(self, index_name, sort_key_name,
                                  sort_key_type=dynamodb.AttributeType.STRING,
                                  projection_type=dynamodb.ProjectionType.KEYS_ONLY):
        index = dynamodb.LocalSecondaryIndexProps(index_name=index_name,
                                                  projection_type=projection_type,
                                                  sort_key=dynamodb.Attribute(name=sort_key_name,
                                                                              type=sort_key_type))
        self.__local_secondary_indexes.append(index)

    def build(self) -> dynamodb.TableV2:
        table = dynamodb.TableV2(self.stack, self.construct_id,
                                 table_name=self.__table_name,
                                 partition_key=self.__partition_key,
                                 sort_key=self.__sort_key,
                                 table_class=self.__table_class,
                                 deletion_protection=self.__deletion_protection,
                                 point_in_time_recovery=self.__point_in_time_recovery,
                                 global_secondary_indexes=self.__global_secondary_indexes,
                                 local_secondary_indexes=self.__local_secondary_indexes)
        return table
