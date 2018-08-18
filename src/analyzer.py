import sqlite3

def parse_settings(settings):
  return None # not used yet

def analyze_sentence(db, sentence, datetime, url):
  for phrase in sentence.noun_phrases:
    if (not db.insert_phrase(datetime, phrase, sentence.polarity, url)):
      return False

  return True

def analyze(db, article):
  from textblob import TextBlob # this is a hack
  blob = TextBlob(article.text)

  for sentence in blob.sentences:
    if (not analyze_sentence(db, sentence, article.publish_date, article.url)):
      return False
  return True

def run(settings, queue, phrases_db):
  running = True

  try:
    while running:
      item = queue.get()
      item.download()
      item.parse()

      if (not analyze(phrases_db, item)):
        print('Unable to analyze article; exiting')
        running = False

  finally:
    None