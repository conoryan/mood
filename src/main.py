#!/usr/local/bin/python3.7

import sys
from multiprocessing import Queue, Process
import configparser
from news_scraper import NewsScraper
import analyzer
from db_handler import DBHandler

def get_settings():
  config = configparser.ConfigParser()
  config.read(sys.argv[1])

  news_settings = config['NEWS_SCRAPER']
  twitter_settings = config['TWITTER_SCRAPER']
  analyzer_settings = config['ANALYZER']
  phrases_db_settings = config['PHRASES_DB']

  return news_settings, twitter_settings, analyzer_settings, phrases_db_settings

if __name__ == "__main__":
  news_settings, twitter_settings, analyzer_settings, phrases_db_settings = get_settings()

  data_q = Queue()
  phrases_db = DBHandler(phrases_db_settings['DBLocation'], 'phrases')

  news = NewsScraper(news_settings, data_q)
  news_proc = Process(target=news.run)
  analyzer_proc = Process(target=analyzer.run, args=(analyzer_settings, 
      data_q, phrases_db))

  news_proc.start()
  analyzer_proc.start()

  try:
    news_proc.join()
    analyzer_proc.join()
  except KeyboardInterrupt:
    sys.exit(0)
