import sys
import newspaper
import configparser
from time import sleep

def parse_settings(settings_filename):
  config = configparser.ConfigParser()
  config.read(settings_filename)
  scraper_settings = config['SCRAPER']

  wait_time = scraper_settings['WaitTime']
  sources = [item.strip() for item in scraper_settings['Sources'].split(',')]

  return wait_time, sources

def run(settings_filename, queue):
  wait_time, source_urls = parse_settings(settings_filename)

  while True:
    for url in source_urls:
      source = newspaper.build(url)
      if (source.size() > 0):
        print('Scraper found ' + str(source.size()) + ' new articles for ' +source.url)
        for article in source.articles:
          queue.put(article)

    sleep(int(wait_time) / 1000.0)