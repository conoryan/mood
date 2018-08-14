#!/usr/local/bin/python3.7

import sys
from multiprocessing import Queue, Process
import configparser
import scraper
import analyzer

def get_settings():
  config = configparser.ConfigParser()
  config.read(sys.argv[1])

  scraper_settings = config['SCRAPER']
  analyzer_settings = config['ANALYZER']

  return scraper_settings, analyzer_settings

if __name__ == "__main__":
  scraper_q = Queue()

  scraper_settings, analyzer_settings = get_settings()
  scraper_proc = Process(target=scraper.run, args=(scraper_settings, scraper_q,))
  analyzer_proc = Process(target=analyzer.run, args=(analyzer_settings, scraper_q,))

  scraper_proc.start()
  analyzer_proc.start()

  try:
    scraper_proc.join()
    analyzer_proc.join()
  except KeyboardInterrupt:
    sys.exit(0)
