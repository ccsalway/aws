import boto3
from config import *

session = boto3.Session(profile_name=PROFILE_NAME)

client = session.client('iam')


def create_group(group_name, path_prefix):
    group = client.create_group(
        Path=path_prefix,
        GroupName=group_name
    )
    return group["Group"]


def attach_policy_managed(group_name, policy_arn):
    client.attach_group_policy(
        GroupName=group_name,
        PolicyArn=policy_arn
    )
    return None


def attach_policy_inline(group_name, policy_name, policy_doc):
    client.put_group_policy(
        GroupName=group_name,
        PolicyName=policy_name,
        PolicyDocument=policy_doc
    )
    return None


def add_user(group_name, user_name):
    client.add_user_to_group(
        GroupName=group_name,
        UserName=user_name
    )
    return None


def get_groups(path_prefix='/'):
    data = client.list_groups(
        PathPrefix=path_prefix
    )
    return [g for g in data["Groups"]]


def get_users(group_name):
    data = client.get_group(
        GroupName=group_name
    )
    return [u for u in data["Users"]]


def get_policies_managed(group_name, path_prefix='/'):
    data = client.list_attached_group_policies(
        GroupName=group_name,
        PathPrefix=path_prefix
    )
    return [p for p in data["AttachedPolicies"]]


def get_policies_inline(group_name):
    data = client.list_group_policies(
        GroupName=group_name
    )
    return [p for p in data["PolicyNames"]]


def delete_group(group_name, path_prefix='/'):
    """The group must not contain any users or have any attached policies."""
    for user in get_users(group_name):
        client.remove_user_from_group(
            GroupName=group_name,
            UserName=user["UserName"]
        )
    for policy in get_policies_managed(group_name, path_prefix):
        client.detach_group_policy(
            GroupName=group_name,
            PolicyArn=policy["PolicyArn"]
        )
    for policy in get_policies_inline(group_name):
        client.delete_group_policy(
            GroupName=group_name,
            PolicyName=policy
        )
    client.delete_group(
        GroupName=group_name
    )
    return None


if __name__ == '__main__':
    for g in get_groups():
        print g
