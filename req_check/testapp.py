from datetime import datetime
from flask import Flask, request, jsonify
import base64
import pickle
import os
from googleapiclient.discovery import build

app = Flask(__name__)

last_history_token = '1'
emails = []
processed_emails = set()

with open('token.pickle', 'rb') as token:
    creds = pickle.load(token)

service = build('gmail', 'v1', credentials=creds)

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

def getPayLoadValueByNames(payload, names):
    d = {}
    for data in payload:
        if data['name'] in names:
            d[data['name']] = data['value']
            names.remove(data['name'])
    return d

@app.route('/')
def homepage():
    the_time = str(datetime.now())

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    """.format(time=the_time)

@app.route('/postNotification',methods=['GET','POST'])
def posting():
    global last_history_token,emails

    if request.method == 'POST':
        content = request.json
        encoded_data = content['message']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        history = ListHistory(service,'me',last_history_token)

        curr_token = None
        for item in history:
            for msg in item['messages']:
                email_id = msg['id']
                last_email = service.users().messages().get(userId='me', id=email_id,format='metadata').execute()
                curr_token = last_email['historyId']
                if curr_token in processed_emails:
                    continue

                relevant_data = getPayLoadValueByNames(last_email['payload']['headers'], {'Subject', 'Date', 'From'})
                relevant_data['body'] = last_email['snippet']
                emails.append(', '.join(['%s:%s'%(k,v) for k,v in relevant_data.items()]))
                processed_emails.add(curr_token)

        last_history_token = curr_token

        return 'success'

    return jsonify(emails)
