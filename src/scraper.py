import abc
from time import sleep

# implementing classes must implement process() and define _wait_time
class Scraper(abc.ABC):
  @abc.abstractmethod
  def process(self):
    pass

  def run(self):
    while True:
      self.process()

      sleep(int(self._wait_time) / 1000.0)