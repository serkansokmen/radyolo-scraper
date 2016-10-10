from flask import Flask, render_template
from tweepy import Stream, API, OAuthHandler, streaming
from tweepy.streaming import StreamListener
from flask_cors import CORS, cross_origin
import pusher

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

consumer_key = '1w5e0y984dXQJJDXMtz8gYhE0'
consumer_secret = 'b8l8xNJArsdK6llySJ4dak3gPsT2RmotKkGx2Y5VwXybfcszLU'
access_token = '17758455-jEPVLA2a7e7XHiaxsXaxR0YzX5cMrb0tXtpPrP8eb'
access_secret = 'qoCY6swRzhXyOThrPzp5nGuYKdRknH2ie0f2nv9HYivRr'

pusher_client = pusher.Pusher(
  app_id='240581',
  key='09a9be90c83a82b77a1a',
  secret='a6626043be057b5c47c7',
  cluster='eu',
  ssl=True
)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitter_api = API(auth)

@app.route('/')
def index(keywords=None):
    return render_template('index.html')

@app.route('/<string:keywords>', methods=['POST'])
def track_keywords(keywords):

    class StreamListener(streaming.StreamListener):
        def on_data(self, data):
            pusher_client.trigger('stream_shannel', 'new_message', data)

        def on_error(self, status):
            print(status)
            return True

    twitter_stream = Stream(auth, StreamListener())
    twitter_stream.filter(track=[keywords])
    return render_template('index.html', {
      'connected': True
    })

if __name__ == '__main__':
    twitter_stream.filter(track=['hello'])

