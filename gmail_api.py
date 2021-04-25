from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
import pandas as pd
from io import StringIO, BytesIO

#############################
# CODE IS FROM GOOGLE QUICKSTART GUIDE
# https://developers.google.com/gmail/api/quickstart/python
#############################

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def GetService():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def GetMessages(service, labelName):
    msg_results = service.users().messages().list(userId='me', q=f'label:{labelName}').execute()
    print(msg_results)
    msgs = msg_results.get('messages', [])

    # if not msgs:
    #     print("No messages found.")
    # else:
    #     print('API_BOX Messages:')
    #     for msg in msgs:
    #         print(msg['id'])
    
    return msgs

def GetAttachement(service, msg_id, user_id='me'):
    """Get and store attachment from Message with given id.

    :param service: Authorized Gmail API service instance.
    :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    :param msg_id: ID of Message containing attachment.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            if part['filename']:
                if 'data' in part['body']:
                    data = part['body']['data']
                else:
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
                    data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = part['filename']
                # with open(path, 'wb') as f:
                #     f.write(file_data)
                return pd.read_csv(BytesIO(file_data))

    except Exception as error:
        print ('An error occurred: %s' % error)

    


if __name__ == '__main__':
    service = GetService()
    msgs = GetMessages(service, labelName='API_BOX')
    GetAttachement(service=service, msg_id=msgs[0]['id'])