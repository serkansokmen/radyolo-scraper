import json
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import tweepy
import pusher


class PusherPipeline(object):

    def __init__(self):
        self.pusher_client = pusher.Pusher(
          app_id=settings['PUSHER_APP_ID'],
          key=settings['PUSHER_KEY'],
          secret=settings['PUSHER_SECRET'],
          cluster=settings['PUSHER_CLUSTER'],
          ssl=True,
        )
        self.auth = tweepy.OAuthHandler(settings['TWITTER_CONSUMER_KEY'], settings['TWITTER_CONSUMER_SECRET'])
        self.auth.set_access_token(settings['TWITTER_ACCESS_TOKEN'], settings['TWITTER_ACCESS_SECRET'])

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))

        if any(txt in item['text'] for txt in settings['RESTRICTS']):
            valid = False
            raise DropItem("Restricted %s !" % item['text'])

        if valid:
            self.pusher_client.trigger('stream_channel', 'new_message', {
                'username': item['username'],
                'text': item['text'],
                'timestamp': item['timestamp'],
            })
        return item
