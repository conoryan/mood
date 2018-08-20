import sqlite3

def parse_settings(settings):
  return None # not used yet

def analyze_sentence(db, sentence, datetime, url):
  for phrase in sentence.noun_phrases:
    db.insert_phrase(datetime, phrase, sentence.polarity, url)

def analyze(db, article):
  from textblob import TextBlob # this is a hack
  blob = TextBlob(article.text)

  for sentence in blob.sentences:
    analyze_sentence(db, sentence, article.publish_date, article.url)

def run(settings, queue, phrases_db):
  try:
    while True:
      item = queue.get()
      item.download()
      item.parse()

      analyze(phrases_db, item)

  finally:
    None