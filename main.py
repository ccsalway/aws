import boto3

from config import *

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

org = session.client('organizations')
s3 = session.client('s3')
iam = session.client('iam')
kms = session.client('kms')

#########################
# Create S3 Buckets
#########################

try:
    s3.create_bucket(
        Bucket=MASTER_ACCOUNT_ALIAS + '.logs',
        CreateBucketConfiguration={
            'LocationConstraint': AWS_REGION
        }
    )
except s3.exceptions.BucketAlreadyOwnedByYou:
    pass
except s3.exceptions.BucketAlreadyExists, e:
    exit(e)

s3.put_bucket_acl(
    Bucket=MASTER_ACCOUNT_ALIAS + '.logs',
    ACL='log-delivery-write'
)
s3.put_bucket_encryption(
    Bucket=MASTER_ACCOUNT_ALIAS + '.logs',
    ServerSideEncryptionConfiguration={
        'Rules': [{
            'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'AES256'
            }
        }]
    }
)
s3.put_bucket_logging(
    Bucket=MASTER_ACCOUNT_ALIAS + '.logs',
    BucketLoggingStatus={
        'LoggingEnabled': {
            'TargetBucket': MASTER_ACCOUNT_ALIAS + '.logs',
            'TargetPrefix': 'logs/'
        }
    }
)

try:
    s3.create_bucket(
        Bucket=MASTER_ACCOUNT_ALIAS + '.users',
        CreateBucketConfiguration={
            'LocationConstraint': AWS_REGION
        }
    )
except s3.exceptions.BucketAlreadyOwnedByYou:
    pass
except s3.exceptions.BucketAlreadyExists, e:
    exit(e)

s3.put_bucket_acl(
    Bucket=MASTER_ACCOUNT_ALIAS + '.users',
    ACL='private'
)
s3.put_bucket_encryption(
    Bucket=MASTER_ACCOUNT_ALIAS + '.users',
    ServerSideEncryptionConfiguration={
        'Rules': [{
            'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'AES256'
            }
        }]
    }
)
s3.put_bucket_logging(
    Bucket=MASTER_ACCOUNT_ALIAS + '.users',
    BucketLoggingStatus={
        'LoggingEnabled': {
            'TargetBucket': MASTER_ACCOUNT_ALIAS + '.logs',
            'TargetPrefix': 'users/'
        }
    }
)

#########################
# Create Organization
#########################

try:
    org.describe_organization()
except org.exceptions.AWSOrganizationsNotInUseException:
    org.create_organization()

#########################
# Setup Account
#########################

iam.update_account_password_policy(
    MinimumPasswordLength=12,
    RequireSymbols=True,
    RequireNumbers=True,
    RequireUppercaseCharacters=True,
    RequireLowercaseCharacters=True,
    AllowUsersToChangePassword=True,
    # MaxPasswordAge=1095,
    # PasswordReusePrevention=1,
    HardExpiry=False
)

account_alias = iam.list_account_aliases()['AccountAliases'][0]

try:
    if account_alias != MASTER_ACCOUNT_ALIAS:
        iam.create_account_alias(
            AccountAlias=MASTER_ACCOUNT_ALIAS
        )
except iam.exceptions.EntityAlreadyExistsException, e:
    exit(e)

#########################
# Create Policies
#########################

repl = {'{{s3prefix}}': MASTER_ACCOUNT_ALIAS}
with open('docs/policies/iamuserselfservice.json') as f:
    policy_document = reduce(lambda a, kv: a.replace(*kv), repl.iteritems(), f.read())

try:
    iam.create_policy(
        PolicyName='IAMUserSelfServicePolicy',
        PolicyDocument=policy_document
    )
except iam.exceptions.EntityAlreadyExistsException:
    # get policy arn
    policies = iam.list_policies(Scope='Local')
    policy_arn = [p for p in policies['Policies'] if p['PolicyName'] == 'IAMUserSelfServicePolicy'][0]['Arn']
    # ensure policy matches
    iam.create_policy_version(
        PolicyArn=policy_arn,
        PolicyDocument=policy_document,
        SetAsDefault=True
    )
    # you can only have 5 versions, so delete any not the default
    policy_versions = iam.list_policy_versions(PolicyArn=policy_arn)
    for p in [v for v in policy_versions['Versions'] if not v['IsDefaultVersion']]:
        iam.delete_policy_version(
            PolicyArn=policy_arn,
            VersionId=p['VersionId']
        )

repl = {}
with open('docs/policies/vpcflowlog.json') as f:
    policy_document = reduce(lambda a, kv: a.replace(*kv), repl.iteritems(), f.read())

try:
    iam.create_policy(
        PolicyName='VPCFlowLogPolicy',
        PolicyDocument=policy_document
    )
except iam.exceptions.EntityAlreadyExistsException:
    # get policy arn
    policies = iam.list_policies(Scope='Local')
    policy_arn = [p for p in policies['Policies'] if p['PolicyName'] == 'VPCFlowLogPolicy'][0]['Arn']
    # ensure policy matches
    iam.create_policy_version(
        PolicyArn=policy_arn,
        PolicyDocument=policy_document,
        SetAsDefault=True
    )
    # you can only have 5 versions, so delete any not the default
    policy_versions = iam.list_policy_versions(PolicyArn=policy_arn)
    for p in [v for v in policy_versions['Versions'] if not v['IsDefaultVersion']]:
        iam.delete_policy_version(
            PolicyArn=policy_arn,
            VersionId=p['VersionId']
        )

repl = {}
with open('docs/policies/ec2vpnserver.json') as f:
    policy_document = reduce(lambda a, kv: a.replace(*kv), repl.iteritems(), f.read())

try:
    iam.create_policy(
        PolicyName='EC2VpnServerPolicy',
        PolicyDocument=policy_document
    )
except iam.exceptions.EntityAlreadyExistsException:
    # get policy arn
    policies = iam.list_policies(Scope='Local')
    policy_arn = [p for p in policies['Policies'] if p['PolicyName'] == 'EC2VpnServerPolicy'][0]['Arn']
    # ensure policy matches
    iam.create_policy_version(
        PolicyArn=policy_arn,
        PolicyDocument=policy_document,
        SetAsDefault=True
    )
    # you can only have 5 versions, so delete any not the default
    policy_versions = iam.list_policy_versions(PolicyArn=policy_arn)
    for p in [v for v in policy_versions['Versions'] if not v['IsDefaultVersion']]:
        iam.delete_policy_version(
            PolicyArn=policy_arn,
            VersionId=p['VersionId']
        )

repl = {'{{s3prefix}}': MASTER_ACCOUNT_ALIAS}
with open('docs/policies/ec2jumpbox.json') as f:
    policy_document = reduce(lambda a, kv: a.replace(*kv), repl.iteritems(), f.read())

try:
    iam.create_policy(
        PolicyName='EC2JumpboxPolicy',
        PolicyDocument=policy_document
    )
except iam.exceptions.EntityAlreadyExistsException:
    # get policy arn
    policies = iam.list_policies(Scope='Local')
    policy_arn = [p for p in policies['Policies'] if p['PolicyName'] == 'EC2JumpboxPolicy'][0]['Arn']
    # ensure policy matches
    iam.create_policy_version(
        PolicyArn=policy_arn,
        PolicyDocument=policy_document,
        SetAsDefault=True
    )
    # you can only have 5 versions, so delete any not the default
    for v in iam.list_policy_versions(PolicyArn=policy_arn)['Versions']:
        if v['IsDefaultVersion']: continue
        iam.delete_policy_version(
            PolicyArn=policy_arn,
            VersionId=v['VersionId']
        )

#########################
# Create Roles
#########################

policies = iam.list_policies(Scope='Local')

repl = {}
with open('docs/policies/ec2assumerole.json') as f:
    policy_document = reduce(lambda a, kv: a.replace(*kv), repl.iteritems(), f.read())

try:
    iam.create_role(
        RoleName='EC2VpnServerRole',
        AssumeRolePolicyDocument=policy_document
    )
    iam.create_instance_profile(
        InstanceProfileName='EC2VpnServerRole'
    )
    iam.add_role_to_instance_profile(
        InstanceProfileName='EC2VpnServerRole',
        RoleName='EC2VpnServerRole'
    )
except iam.exceptions.EntityAlreadyExistsException:
    pass

policy_arn = [p for p in policies['Policies'] if p['PolicyName'] == 'EC2VpnServerPolicy'][0]['Arn']
iam.attach_role_policy(
    RoleName='EC2VpnServerRole',
    PolicyArn=policy_arn
)

try:
    iam.create_role(
        RoleName='EC2JumpboxRole',
        AssumeRolePolicyDocument=policy_document
    )
    iam.create_instance_profile(
        InstanceProfileName='EC2JumpboxRole'
    )
    iam.add_role_to_instance_profile(
        InstanceProfileName='EC2JumpboxRole',
        RoleName='EC2JumpboxRole'
    )
except iam.exceptions.EntityAlreadyExistsException:
    pass

policy_arn = [p for p in policies['Policies'] if p['PolicyName'] == 'EC2JumpboxPolicy'][0]['Arn']
iam.attach_role_policy(
    RoleName='EC2JumpboxRole',
    PolicyArn=policy_arn
)

#########################
# Create Groups
#########################

policies = iam.list_policies(Scope='Local')

try:
    iam.create_group(
        GroupName='Everyone'
    )
except iam.exceptions.EntityAlreadyExistsException:
    pass

policy_arn = [p for p in policies['Policies'] if p['PolicyName'] == 'IAMUserSelfServicePolicy'][0]['Arn']
iam.attach_group_policy(
    GroupName='Everyone',
    PolicyArn=policy_arn
)

try:
    iam.create_group(
        GroupName='VPN1Users'
    )
except iam.exceptions.EntityAlreadyExistsException:
    pass

#########################
# Create KMS Keys
#########################

create = True
for a in kms.list_aliases()['Aliases']:
    if a['AliasName'] != 'alias/ec2-ebs-key' or not kms.describe_key(KeyId=a['TargetKeyId'])['KeyMetadata']['Enabled']:
        continue
    create = False

if create:
    data = kms.create_key()['KeyMetadata']
    try:
        kms.create_alias(
            AliasName='alias/ec2-ebs-key',
            TargetKeyId=data['KeyId']
        )
    except kms.exceptions.AlreadyExistsException:
        kms.update_alias(
            AliasName='alias/ec2-ebs-key',
            TargetKeyId=data['KeyId']
        )

#########################
# Create VPC
#########################
