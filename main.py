from config import *
import boto3

import sys

for arg in sys.argv:
    print arg

session = boto3.Session(aws_access_key_id=PROFILE_NAME, aws_secret_access_key=)


if __name__ == '__main__':
    pass