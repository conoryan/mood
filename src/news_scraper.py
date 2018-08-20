import newspaper
from scraper import Scraper
from time import sleep

class NewsScraper(Scraper):
  def __init__(self, settings, queue):
    Scraper.__init__(self, settings, queue)
    self._wait_time = settings['WaitTime']
    self._source_urls = [item.strip() for item in settings['Sources'].split(',')]

  def before(self):
    pass

  def process(self):
    for url in self._source_urls:
      source = newspaper.build(url, memoize_articles=False)
      if (source.size() > 0):
        print('NewsScraper found ' + str(source.size()) + ' new articles for ' 
              +source.url)
        for article in source.articles:
          self._data_queue.put(article)

  def delay(self):
    sleep(int(self._wait_time) / 1000.0)