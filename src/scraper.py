import abc
from time import sleep

# implementing classes must implement process() and delay(). delay is called
# after process, continuously
# pass in to consturctor: (1) configparser with settins defined,
#   (2) queue to push data gained from process() onto
class Scraper(abc.ABC):
  def __init__(self, settings, queue):
    self._data_queue = queue

  @abc.abstractmethod
  def before(self):
    pass

  @abc.abstractmethod
  def process(self):
    pass

  @abc.abstractmethod
  def delay(self):
    pass

  def run(self):
    self.before()

    while True:
      self.process()
      self.delay()