from scraper import Scraper
import tweepy
from time import sleep

class TwitterScraper(Scraper):
  def __init__(self, settings, queue):
    Scraper.__init__(self, settings, queue)
    self._wait_time = settings['WaitTime']

  def before(self):
    # TODO catch up to now based on last date in table - go back 7 days
    pass

  def process(self):
    '''api.search
    q="*"
    rpp=100
    tweet_mode="extended"
    result_type="popular"
    lang="en"'''



    print("twitter scraped")

  def delay(self):
    # TODO make delay for wake @ given GatherTime
    # TODO remove wait_time
    sleep(int(self._wait_time) / 1000.0)