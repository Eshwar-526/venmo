import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


# def main():
#   """Shows basic usage of the Gmail API.
#   Lists the user's Gmail labels.
#   """
#   creds = None
#   # The file token.json stores the user's access and refresh tokens, and is
#   # created automatically when the authorization flow completes for the first
#   # time.
#   if os.path.exists("token.json"):
#     creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#   # If there are no (valid) credentials available, let the user log in.
#   if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#       creds.refresh(Request())
#     else:
#       flow = InstalledAppFlow.from_client_secrets_file(
#           "credentials.json", SCOPES
#       )
#       creds = flow.run_local_server(port=0)
#     # Save the credentials for the next run
#     with open("token.json", "w") as token:
#       token.write(creds.to_json())

#   try:
#     # Call the Gmail API
#     service = build("gmail", "v1", credentials=creds)
#     # results = service.users().labels().list(userId="me").execute()
#     results = service.users().messages().list(userId='me',maxResults=20,labelIds = ['INBOX']).execute()
#     print(results)

#     labels = results.get("labels", [])

#     if not labels:
#       print("No labels found.")
#       return
#     print("Labels:")
#     # print(labels)
#     # for label in labels:
#     #   print(label["name"])

#   except HttpError as error:
#     # TODO(developer) - Handle errors from gmail API.
#     print(f"An error occurred: {error}")


import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
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

    return creds

# def get_last_inbox_message():
#     creds = authenticate_gmail()
#     service = build('gmail', 'v1', credentials=creds)

#     # Call the Gmail API
#     results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
#     messages = results.get('messages', [])

#     if not messages:
#         print('No messages found.')
#         return

#     message_id = messages[0]['id']
#     message = service.users().messages().get(userId='me', id=message_id).execute()

#     print('Message snippet:', message['snippet'])
#     print('Message details:', message)

from base64 import urlsafe_b64decode
import re

def get_last_inbox_message():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
        return

    message_id = messages[0]['id']
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()

    headers = message['payload']['headers']
    subject = next(header['value'] for header in headers if header['name'] == 'Subject')
    sender = next(header['value'] for header in headers if header['name'] == 'From')

    # Decode the email body
    parts = message['payload'].get('parts')
    if not parts:
        body = message['payload']['body']['data']
    else:
        part = next(part for part in parts if part['mimeType'] == 'text/plain')
        body = part['body']['data']

    decoded_body = urlsafe_b64decode(body).decode('utf-8')

    print(f'Subject: {subject}')
    print(f'From: {sender}')
    print(f'Body: {decoded_body}')



def main():
    get_last_inbox_message()
    # this is a test commit

if __name__=="__main__": 
    main() 

