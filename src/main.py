#!/usr/local/bin/python3.7

import sys
from multiprocessing import Queue, Process
import scraper
import analyzer

if __name__ == "__main__":
  scraper_q = Queue()

  scraper_proc = Process(target=scraper.run, args=(sys.argv[1], scraper_q,))
  analyzer_proc = Process(target=analyzer.run, args=(sys.argv[1], scraper_q,))

  scraper_proc.start()
  analyzer_proc.start()

  scraper_proc.join()
  analyzer_proc.join()
