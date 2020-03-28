import json
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    s3client = boto3.client('s3')
    paginator = s3client.get_paginator('list_objects_v2')
    page_iter = paginator.paginate(Bucket='', Prefix='')

    objects = []
    for item in page_iter:
        objects = objects + item['Contents']

    get_last_modified = lambda obj: obj['LastModified']

    most_recent_file = [obj for obj in sorted(objects, key=get_last_modified, reverse=True)][0]

    now = datetime.now()
    if now-timedelta(hours=24) <= most_recent_file['LastModified'] <= now:
        print(now)

lambda_handler(None, None)