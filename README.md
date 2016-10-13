# radyolo scraper

twitter streaming api scraper and pusher

v1.1.0

### Installation

```sh
$ git clone git@github.com:serkansokmen/radyolo-scraper.git
$ cd radyolo-scraper
$ pip install -r requirements.txt
```

Adjust `settings.py` like following:

- Duplicate `settings.default.py` as `settings.py`
- Create a [Twitter Application](https://dev.twitter.com) twitter application and enter keys
- Create a [Pusher Application](https://pusher.com) and enter keys
- edit `RESTRICTS` as deserved

### Running

```sh
$ scrapy crawl stream-spider -a track=hello -o track/hello.json -t json
```
