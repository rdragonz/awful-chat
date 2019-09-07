import flask
from flask import render_template
import redis
import urllib
app = flask.Flask(__name__)
red = redis.StrictRedis()


def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('chat')
    for message in pubsub.listen():
        print message
        yield 'data: %s\n\n' % message['data']

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/stream')
def stream():
    return flask.Response(event_stream(), mimetype="text/event-stream")

@app.route('/chat_history')
def chat_history():
    return render_template('chat_history.html')

@app.route('/post', methods=['POST', 'GET'])
def post():
    message = urllib.unquote(flask.request.get_data()[8:])
    red.publish('chat', u'%s' % (message))
    chat_history = open("templates/chat_history.html", "a")
    chat_history.write(message + '<br>\n')
    print("Appended message")
    chat_history.close()


    return flask.Response(status=204)

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

app.debug = True
app.run(debug=True, host='0.0.0.0', port=80)