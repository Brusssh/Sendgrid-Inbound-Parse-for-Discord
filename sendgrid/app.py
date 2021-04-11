import json
import base64
import io
import os

import requests
from datetime import datetime
import cgi


def lambda_handler(event, context):
    body = event['body'].encode("utf-8")
    fp = io.BytesIO(body)

    environ = {'REQUEST_METHOD': 'POST'}
    header = {
        'content-type': event['headers']['Content-Type'],
        'content-length': len(body)
    }

    webhook_url = os.getenv("DiscordWebhookEnv", "")

    fs = cgi.FieldStorage(fp=fp, environ=environ, headers=header)

    main_content = {
        "username": "Mail Notification: " + fs.getvalue("from", "From Unknown"),
        "content": "```\n" +
                   "To: " + fs.getvalue("to", "To Unknown") + "\n" +
                   "Subject: " + fs.getvalue("subject", "Subject Unknown") + "\n" +
                   "Body: " + fs.getvalue("text", "Text Unknown") + "\n" +
                   "```"
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(webhook_url, json.dumps(main_content), headers=headers)
    return {
        'statusCode': 200,
        'body': json.dumps(response.status_code)
    }
