import json
import boto3
import os
from datetime import datetime, timedelta, timezone

def lambda_handler(event, context):
    s3client = boto3.client('s3')
    paginator = s3client.get_paginator('list_objects_v2')
    page_iter = paginator.paginate(Bucket=os.environ['bucket_name'], Prefix=os.environ['prefix'])

    objects = []
    for item in page_iter:
        objects = objects + item['Contents']

    get_last_modified = lambda obj: obj['LastModified']

    most_recent_file = [obj for obj in sorted(objects, key=get_last_modified, reverse=True)][0]

    now = datetime.now(timezone.utc)
    # If it was within the past 24 hours
    if now-timedelta(hours=24) <= most_recent_file['LastModified'] <= now:
        None # Everything checked out
    else:
        # Alert on the failure
        client = boto3.client("sns")
        client.publish(
            Message="Backups did not complete! You should check them when you can.",
            TopicArn=os.environ['topic_arn']
        )