import os

'''
Boto3 searches for credentials in:

1. Passing credentials as parameters in the boto.client() method
2. Passing credentials as parameters when creating a Session object
3. Environment variables
4. Shared credential file (~/.aws/credentials)
5. AWS config file (~/.aws/config)
6. Assume Role provider
7. Boto2 config file (/etc/boto.cfg and ~/.boto)
8. Instance metadata service on an Amazon EC2 instance that has an IAM role configured.
'''

AWS_REGION = 'eu-west-1'
AWS_ACCOUNT_ID = os.environ["AWS_ACCOUNT_ID"]
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

MASTER_ACCOUNT_ALIAS = 'aws-pod-dev'
