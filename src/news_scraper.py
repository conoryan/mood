import newspaper
from scraper import Scraper
from time import sleep
import csv

class NewsScraper(Scraper):
  def __init__(self, settings, queue):
    Scraper.__init__(self, settings, queue)
    self._wait_time = settings['WaitTime']
    self._full_refresh_start = settings['FullRefreshStart'] == 'True'

    self._source_urls = {}
    with open(settings['SourcesFile'], newline='', encoding='utf-8-sig') as f:
      reader = csv.reader(f)
      next(reader)
      for row in reader:
        self._source_urls[row[0]] = int(row[1])

  def _empty_source(self, source, url):
    print('NewsScraper found ' + str(source.size()) + ' new articles for ' 
          +source.url)
    for article in source.articles:
      article.url_root = url
      self._data_queue.put(article)

  def before(self):
    if self._full_refresh_start:
      for url in self._source_urls:
        source = newspaper.build(url, memoize_articles=False)
        if (source.size() > 0):
          self._empty_source(source, url)

  def process(self):
    for url in self._source_urls:
      source = newspaper.build(url, memoize_articles=True)
      if (source.size() > 0):
        self._empty_source(source, url)

  def delay(self):
    sleep(int(self._wait_time) / 1000.0)