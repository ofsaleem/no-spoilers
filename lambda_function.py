'''
This function handles a Slack slash command and echoes the details back to the user.

Follow these steps to configure the slash command in Slack:

  1. Navigate to https://<your-team-domain>.slack.com/services/new

  2. Search for and select "Slash Commands".

  3. Enter a name for your command and click "Add Slash Command Integration".

  4. Copy the token string from the integration settings and use it in the next section.

  5. After you complete this blueprint, enter the provided API endpoint URL in the URL field.


To encrypt your secrets use the following steps:

  1. Create or use an existing KMS Key - http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html

  2. Click the "Enable Encryption Helpers" checkbox

  3. Paste <COMMAND_TOKEN> into the kmsEncryptedToken environment variable and click encrypt


Follow these steps to complete the configuration of your command API endpoint

  1. When completing the blueprint configuration select "Open" for security
     on the "Configure triggers" page.

  2. Enter a name for your execution role in the "Role name" field.
     Your function's execution role needs kms:Decrypt permissions. We have
     pre-selected the "KMS decryption permissions" policy template that will
     automatically add these permissions.

  3. Update the URL for your Slack slash command with the invocation URL for the
     created API resource in the prod stage.
'''

import boto3
import sys
import json
import logging
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from base64 import b64decode
from urllib.parse import parse_qs, urlencode


#ENCRYPTED_EXPECTED_TOKEN = 

#kms = boto3.client('kms')
#expected_token = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext']

expected_token = "REDACTED"
#put token here

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    params = parse_qs(event['body'])
    token = params['token'][0]
    if token != expected_token:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Exception('Invalid request token'))
    user = params['user_name'][0]
    command = params['command'][0]
    channel = params['channel_name'][0]
    if 'text' not in params:
        return { 'text': 'Sorry! You need to include a spoiler.', 'response_type': 'ephemeral' }
    response_url = params['response_url']
    all_text = params['text'][0]
    heading = "Incoming spoiler from %s: " % (user)
    split_text = all_text.split('[')
    spoiler_text = split_text[0]
    headers = {'content-type': 'application/json'}
    url = response_url[0]
    print(url)
    if len(split_text) > 1:
        caption_text = split_text[1].strip(']')
        final_message = ". \n \n \n \n \n \n \n" + spoiler_text
        final_message = final_message.replace('"','\\"')
        caption_text = caption_text.replace('"','\\"')
        payload = '{ "response_type": "in_channel", "attachments": [ { "text": "%s", "pretext": "%s", "attachment_type": "text", "color": "#00bbff", "title": "%s" } ] }' % (final_message, heading, caption_text)
        print(payload)
        payload = payload.encode("utf-8")
        request = Request(url, data=payload, headers=headers)
        response = urlopen(request)
        return { 'text': 'hiding spoiler...', 'response_type': 'ephemeral' }
    final_message = ". \n \n \n \n \n \n \n" + spoiler_text
    final_message = final_message.replace('"','\\"')
    payload = '{ "response_type": "in_channel", "attachments": [ { "text": "%s", "pretext": "%s", "attachment_type": "text", "color": "#00bbff" } ] }' % (final_message, heading)
    print (payload)
    payload = payload.encode("utf-8")
    request = Request(url, data=payload, headers=headers)
    response = urlopen(request)
    return { 'text': 'hiding spoiler...', 'response_type': 'ephemeral' }
