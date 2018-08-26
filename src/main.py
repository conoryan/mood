#!/usr/local/bin/python3.7

import sys
from multiprocessing import Queue, Process
import configparser
from news_scraper import NewsScraper
from twitter_scraper import TwitterScraper
import analyzer
from news_db_handler import NewsDBHandler
from twitter_db_handler import TwitterDBHandler
from mood_generator import MoodGenerator
from datetime import datetime

def get_settings():
  config = configparser.ConfigParser()
  config.read(sys.argv[1])

  news_settings = config['NEWS_SCRAPER']
  twitter_settings = config['TWITTER_SCRAPER']
  analyzer_settings = config['ANALYZER']
  news_db_settings = config['NEWS_DB']
  twitter_db_settings = config['TWITTER_DB']

  return (news_settings, twitter_settings, analyzer_settings, news_db_settings, 
          twitter_db_settings)

if __name__ == "__main__":
  (news_settings, twitter_settings, analyzer_settings, news_db_settings, 
    twitter_db_settings) = get_settings()

  data_q = Queue()
  news_db = NewsDBHandler(news_db_settings['DBLocation'], 'news_phrases')
  twitter_db = TwitterDBHandler(twitter_db_settings['DBLocation'], 'tweet_phrases')

  news = NewsScraper(news_settings, data_q)
  twitter = TwitterScraper(twitter_settings, data_q)
  news_proc = Process(target=news.run)
  twitter_proc = Process(target=twitter.run)
  analyzer_proc = Process(target=analyzer.run, args=(analyzer_settings, 
      data_q, news_db, twitter_db))

  news_proc.start()
  twitter_proc.start()
  analyzer_proc.start()

  mood = MoodGenerator(news_db, twitter_db, news._source_urls)
  print(mood.get_score('space', 
                       datetime.strptime("2017-08-21 00:00:00", "%Y-%m-%d %H:%M:%S"), 
                       datetime.strptime("2018-08-21 23:59:59", "%Y-%m-%d %H:%M:%S")))

  try:
    news_proc.join()
    twitter_proc.join()
    analyzer_proc.join()
  except KeyboardInterrupt:
    sys.exit(0)
