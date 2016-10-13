import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import pusher
import tweepy
import json


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
        if valid:
            self.pusher_client.trigger('stream_shannel', 'new_message', {
                'username': item['username'],
                'text': item['text'],
                'timestamp': item['timestamp'],
            })
            log.msg("Pusher message sent!",
                level=log.DEBUG, spider=spider)
        return item


# class MongoDBPipeline(object):

#     def __init__(self):
#         connection = pymongo.MongoClient(
#             settings['MONGODB_SERVER'],
#             settings['MONGODB_PORT']
#         )
#         db = connection[settings['MONGODB_DB']]
#         self.collection = db[settings['MONGODB_COLLECTION']]

#     def process_item(self, item, spider):
#         valid = True
#         for data in item:
#             if not data:
#                 valid = False
#                 raise DropItem("Missing {0}!".format(data))
#         if valid:
#             self.collection.insert(dict(item))
#             log.msg("Message added to MongoDB database!",
#                     level=log.DEBUG, spider=spider)
#         return item
