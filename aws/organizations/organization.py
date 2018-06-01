import boto3

from config import *


class Main(object):

    def __init__(self, session):
        self.client = session.client('organizations')

    def get_client(self):
        return self.client

    def list_accounts(self):
        return self.client.list_accounts()


if __name__ == '__main__':
    session = boto3.Session(profile_name=AWS_PROFILE)

    client = Main(session).get_client()
    try:
        client.list_accounts()
    except client.exceptions.AWSOrganizationsNotInUseException, e:
        print e
