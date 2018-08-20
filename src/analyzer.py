import sqlite3
import newspaper

def parse_settings(settings):
  pass # not used yet

def analyze_news_sentence(news_db, sentence, datetime, url):
  for phrase in sentence.noun_phrases:
    news_db.insert_phrase(datetime, phrase, sentence.polarity, url)

def analyze_article(news_db, article):
  article.download()
  article.parse()

  from textblob import TextBlob # this is a hack
  blob = TextBlob(article.text)
  for sentence in blob.sentences:
    analyze_news_sentence(news_db, sentence, article.publish_date, article.url)

def run(settings, queue, news_db, twitter_db):
  try:
    while True:
      item = queue.get()

      if (type(item) is newspaper.article.Article):
        analyze_article(news_db, item)
      else: # TODO check for twitter object type
        pass

  finally:
    pass