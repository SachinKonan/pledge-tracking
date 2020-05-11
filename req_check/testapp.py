from datetime import datetime
from flask import Flask, request, jsonify
import base64

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
        data.append(base64.decode(content['data']))
        return 'success'

    return jsonify(data)
