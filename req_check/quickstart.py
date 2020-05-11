from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def ListHistory(service, user_id, start_history_id='1'):
    try:
        history = (service.users().history().list(userId=user_id,
                                                  startHistoryId=start_history_id)
                   .execute())
        changes = history['history'] if 'history' in history else []
        while 'nextPageToken' in history:
            page_token = history['nextPageToken']
            history = (service.users().history().list(userId=user_id,
                                                      startHistoryId=start_history_id,
                                                      pageToken=page_token).execute())
            changes.extend(history['history'])

        return changes
    except Exception as e:
        raise e

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../token.pickle'):
        with open('../token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/gtakpsi-rush/topics/gmailTrigger'
    }
    #o = service.users().watch(userId='me', body=request).execute()

    history = ListHistory(service,'me',1)
    pprint(history)

    """
    for item in history:
        for msg in item['messages']:
            email_id = msg['id']
            msg = service.users().messages().get(userId='me', id=email_id,format='metadata').execute()
            print(msg)
            if msg['historyId'] == '2264':
                print(msg['snippet'])
                for header in msg['payload']['headers']:
                    if header['name'] == 'From':

                        print(header['value'])
    """







if __name__ == '__main__':
    main()