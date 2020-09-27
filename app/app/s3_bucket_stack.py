from aws_cdk import(
    core,
    aws_iam as iam,
    aws_s3 as s3
)

class S3BucketStack(core.Stack):

    def __init__(self,scope:core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope,id,**kwargs)

        self.source_bucket_name_prefix = 'source-s3-bucket-replication-demo'
        self.destination_bucket_name_prefix='destination-s3-bucket-replication-demo'

        if(self.region == 'us-east-1'):
            self.role=iam.Role(
                self,
                's3_replica_poc_role',
                assumed_by=iam.ServicePrincipal('s3.amazonaws.com'),
                role_name=f's3-replication-role'
            )

            iam.Policy(
                self,
                's3_replica_poc_policy',
                roles=[
                    self.role
                ],
                    statements=[
                        self.replication_source_policy(self.get_bucket_arn(self.source_bucket_name_prefix,'us-east-1')),
                        self.replication_policy(self.get_bucket_arn(self.destination_bucket_name_prefix,'us-west-2'))
                    ]
                
            )
            

            self.replication_conf = s3.CfnBucket.ReplicationConfigurationProperty(
                role=self.role.role_arn,
                rules=[
                    s3.CfnBucket.ReplicationRuleProperty(
                        id='rule-replicate-all-data',
                        destination=s3.CfnBucket.ReplicationDestinationProperty(
                            bucket=self.get_bucket_arn(self.destination_bucket_name_prefix,'us-west-2')
                        ),
                    prefix='testing/',
                    status='Enabled'
                    )             
                ]
            )

            s3.CfnBucket(
                self,
                'Bucket-id',
                access_control='Private',
                bucket_name=f'{self.source_bucket_name_prefix}-{self.region}',
                versioning_configuration = s3.CfnBucket.VersioningConfigurationProperty(
                    status='Enabled'
                ),
                replication_configuration=self.replication_conf
            )

        elif(self.region == 'us-west-2'):
            s3.CfnBucket(
                self,
                'Bucket-id',
                access_control='Private',
                bucket_name=f'{self.destination_bucket_name_prefix}-{self.region}',
                versioning_configuration = s3.CfnBucket.VersioningConfigurationProperty(
                    status='Enabled'
                )
            )

    @staticmethod
    def replication_source_policy(source_bucket):
        return iam.PolicyStatement(
            actions=[
                's3:ListBucket',
                's3:GetReplicationConfiguration',
                's3:GetObjectVersionForReplication',
                's3:GetObjectVersionAcl',
                's3:GetObjectVersionTagging',
                's3:GetObjectRetention',
                's3:GetObjectLegalHold'
            ],
            effect=iam.Effect.ALLOW,
            resources=[
                source_bucket,
                f'{source_bucket}/*']
        )

    @staticmethod
    def get_bucket_arn(bucket_name_prefix,region):
        return f'arn:aws:s3:::{bucket_name_prefix}-{region}'.lower()

    @staticmethod
    def replication_policy(destination_bucket_arn):
        return iam.PolicyStatement(
            actions=[
                's3:ReplicateObject',
                's3:ReplicateDelete',
                's3:ReplicateTag',
                's3:GetObjectVersionTagging'
            ],
            effect=iam.Effect.ALLOW,
            resources=[
                f'{destination_bucket_arn}/*'
            ]
        )