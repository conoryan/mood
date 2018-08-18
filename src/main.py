#!/usr/local/bin/python3.7

import sys
from multiprocessing import Queue, Process
import configparser
import scraper
import analyzer
from db_handler import DBHandler

def get_settings():
  config = configparser.ConfigParser()
  config.read(sys.argv[1])

  scraper_settings = config['SCRAPER']
  analyzer_settings = config['ANALYZER']
  phrases_db_settings = config['PHRASES_DB']

  return scraper_settings, analyzer_settings, phrases_db_settings

if __name__ == "__main__":
  scraper_settings, analyzer_settings, phrases_db_settings = get_settings()

  scraper_q = Queue()
  phrases_db = DBHandler(phrases_db_settings['DBLocation'], 'phrases')
  if (not phrases_db.is_init()):
    sys.exit(1)

  scraper_proc = Process(target=scraper.run, args=(scraper_settings, scraper_q,))
  analyzer_proc = Process(target=analyzer.run, args=(analyzer_settings, 
      scraper_q, phrases_db))

  scraper_proc.start()
  analyzer_proc.start()

  try:
    scraper_proc.join()
    analyzer_proc.join()
  except KeyboardInterrupt:
    sys.exit(0)
