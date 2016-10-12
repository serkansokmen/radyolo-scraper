import json
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS, cross_origin
from tweepy import Stream, API, OAuthHandler, streaming
from tweepy.streaming import StreamListener
import pusher

app = Flask(__name__)
app.config.update(
  DEBUG=True,
  SECRET_KEY='topsecret',
  PUSHER_CONSUMER_KEY='1w5e0y984dXQJJDXMtz8gYhE0',
  PUSHER_CONSUMER_SECRET='b8l8xNJArsdK6llySJ4dak3gPsT2RmotKkGx2Y5VwXybfcszLU',
  PUSHER_ACCESS_TOKEN='17758455-jEPVLA2a7e7XHiaxsXaxR0YzX5cMrb0tXtpPrP8eb',
  PUSHER_ACCESS_SECRET='qoCY6swRzhXyOThrPzp5nGuYKdRknH2ie0f2nv9HYivRr',
)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
toolbar = DebugToolbarExtension(app)

pusher_client = pusher.Pusher(
  app_id='240581',
  key='09a9be90c83a82b77a1a',
  secret='a6626043be057b5c47c7',
  cluster='eu',
  ssl=True
)

auth = OAuthHandler(app.config['PUSHER_CONSUMER_KEY'], app.config['PUSHER_CONSUMER_SECRET'])
auth.set_access_token(app.config['PUSHER_ACCESS_TOKEN'], app.config['PUSHER_ACCESS_SECRET'])
twitter_api = API(auth)

@app.route('/')
def home(keywords=None):
    twitter_stream = Stream(auth, StreamListener())
    twitter_stream.filter(track=['hello'])
    return render_template('home.html')


@app.route('/<string:keywords>', methods=['GET'])
def track_keywords(keywords):
  twitter_stream = Stream(auth, StreamListener())
  twitter_stream.filter(track=[keywords])
  return render_template('home.html')

class StreamListener(streaming.StreamListener):

    def on_data(self, data):
        result = json.loads(data)
        # disallowed_keys = ['retweeted', 'retweeted_status', 'is_quote_status']
        if result.get('retweeted_status') or result.get('is_quote_status'):
            return

        username = result.get('user').get('screen_name')
        message = result.get('text')

        if any(x in message for x in ['http://', 'https://', '@']):
            return
        # print '%s: %s' % (username, message)
        # print '%s' % (message)
        pusher_client.trigger('stream_shannel', 'new_message', result)

    def on_error(self, status):
        print(status)
        return True



# with app.get_context():
#     track_keywords('hello')

