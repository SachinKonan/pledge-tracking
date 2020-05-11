from datetime import datetime
from flask import Flask, request, jsonify
import base64
import json

app = Flask(__name__)
data = []

@app.route('/')
def homepage():
    the_time = str(datetime.now())

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    """.format(time=the_time)

@app.route('/postNotification',methods=['GET','POST'])
def posting():
    if request.method == 'POST':
        content = request.json
        encoded_data = content['message']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        data.append(json.loads(decoded_data))
        return 'success'

    return jsonify(data)
