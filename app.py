import flask
from flask import render_template
import redis
import urllib
app = flask.Flask(__name__) #init flask
red = redis.StrictRedis() #Listen for redis


def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('chat') #subscribe to run this function on all chat events
    for message in pubsub.listen():
        print message
        yield 'data: %s\n\n' % message['data'] #return a properly formatted server side event

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/stream')
def stream():
    return flask.Response(event_stream(), mimetype="text/event-stream") #return the event stream with the proper mime so that chrome is happy

@app.route('/chat_history')
def chat_history():
    return render_template('chat_history.html')

@app.route('/post', methods=['POST', 'GET'])
def post():
    message = urllib.unquote(flask.request.get_data()[8:]) #get the message, trim off the "message=" part, and then unescape it so we can XSS
    red.publish('chat', u'%s' % (message)) #publish a chat event on recieving a message
    chat_history = open("templates/chat_history.html", "a") #Open the chat_history file for writing
    chat_history.write(message + '<br>\n') #Write the history plus a linebreak so that it stays consistent with the other messages
    print("Appended message")
    chat_history.close() #Close the file to write changes to disk


    return flask.Response(status=204) #Return a no content so that chrome is happy

@app.after_request
def set_response_headers(response):
    #This function runs after each request and tells the browser not to cache anything. This is useful because the chat history is constantly updating.
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

app.debug = True #Run in debug mode because for some reason it doesn't run in normal mode?
app.run(debug=True, host='0.0.0.0', port=80) #Run the app on port 80