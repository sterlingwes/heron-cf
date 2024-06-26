import boto3
import os
import json


def lambda_handler(event, context):
    payload = json.loads(event["Records"][0]["body"])
    date = payload["date"]
    identityid = payload["identityID"]
    ssm = boto3.client("ssm")
    video_domain_param = ssm.get_parameter(
        Name="/heron/heron-video-domain", WithDecryption=False
    )
    video_domain = video_domain_param["Parameter"]["Value"]

    ses = boto3.client("ses")
    response = ses.send_email(
        Source=os.environ["SOURCEEMAIL"],
        Destination={
            "ToAddresses": [
                payload["config"]["destination"],
            ]
        },
        Message={
            "Subject": {
                "Data": "Update Livestream from heron user",
            },
            "Body": {
                "Text": {
                    "Data": "There is a live stream going"
                    + "on now at this link\n"
                    + "https://"
                    + video_domain
                    + "/index.html?identityId="
                    + identityid
                    + "&timestamp="
                    + date,
                }
            },
        }
    )
    print(response)
