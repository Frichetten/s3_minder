# s3_minder

Lambda function to detect if files have been uploaded to an S3 bucket by a certain time.

## What is This?

I perform incremental backups of data and store them in AWS S3 on a regular basis. One concern I have is knowing if something goes wrong with the server. What if the box has a meltdown and I come to find out it hasn't been doing backups for 6 months?

My solution is this Lambda function that runs on a cronjob. Every few days it will check if new data has been uploaded to S3. If it doesn't find anything newer than 24 hours it will send a message through an SNS publish.

## How Can I Use This?

Setup is simple. Copy and pase the index.py file into your Lambda function. Then provide IAM permissions to list the objects of the S3 bucket. Finally create an SNS topic, subscribe to it with you phone, and provide the permissions to IAM. An example is shown below.

<pre><code>{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sns:Publish",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:sns:region:************:sns_topic",
                "arn:aws:s3:::super-cool-bucket-name"
            ]
        }
    ]
}</code></pre>
