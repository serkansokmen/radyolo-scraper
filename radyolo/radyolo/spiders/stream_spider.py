# -*- coding: utf-8 -*-
import scrapy
import tweepy
import scrapy_twitter
from radyolo.items import StreamItem


class StreamSpider(scrapy.Spider):
    name = 'stream-spider'
    allowed_domains = ['twitter.com']

    def __init__(self, track=None, *args, **kwargs):
        if not track:
            raise scrapy.exceptions.CloseSpider('Argument track not set.')
        super(StreamSpider, self).__init__(*args, **kwargs)
        self.track = track.split(',')

    def start_requests(self):
        return [scrapy_twitter.TwitterStreamFilterRequest(track=self.track)]

    def parse(self, response):
        tweets = response.tweets

        for tweet in tweets:
            tweet_item = scrapy_twitter.to_item(tweet)
            yield StreamItem(
                username=tweet_item['user']['screen_name'],
                text=tweet_item['text'],
                timestamp=tweet_item['timestamp_ms'])

