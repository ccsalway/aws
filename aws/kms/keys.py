import boto3
from config import *

session = boto3.Session(profile_name=PROFILE_NAME)

client = session.client('kms')


def create_key():
    data = client.create_key()
    return data["KeyMetadata"]


def schedule_key_deletion(target_keyid, pending_window=7):
    client.schedule_key_deletion(
        KeyId=target_keyid,
        PendingWindowInDays=pending_window
    )


def create_alias(alias_name, target_keyid):
    client.create_alias(
        AliasName='alias/' + alias_name,
        TargetKeyId=target_keyid
    )
    return None


def delete_alias(alias_name):
    client.delete_alias(
        AliasName='alias/' + alias_name
    )
    return None


def update_alias(alias_name, target_keyid):
    client.update_alias(
        AliasName='alias/' + alias_name,
        TargetKeyId=target_keyid
    )
    return None


if __name__ == '__main__':
    keyid = create_key()["KeyId"]
    try:
        create_alias("gateway/test", keyid)
    except Exception, e:
        update_alias('gateway/test', keyid)
        print e
