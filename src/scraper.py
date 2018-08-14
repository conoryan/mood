import sys
import newspaper
from time import sleep

def parse_settings(settings):
  wait_time = settings['WaitTime']
  sources = [item.strip() for item in settings['Sources'].split(',')]

  return wait_time, sources

def run(settings, queue):
  wait_time, source_urls = parse_settings(settings)

  while True:
    for url in source_urls:
      source = newspaper.build(url)
      if (source.size() > 0):
        print('Scraper found ' + str(source.size()) + ' new articles for ' +source.url)
        for article in source.articles:
          queue.put(article)

    sleep(int(wait_time) / 1000.0)