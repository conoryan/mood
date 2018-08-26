import sqlite3
import newspaper
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import wordninja
from datetime import datetime

def parse_settings(settings):
  pass # not used yet

def _consume_article(news_db, article):
  if (article.publish_date is None):
    print("Skipping %s; article has no date" %(article.url,))
    return

  from textblob import TextBlob # this is a hack
  blob = TextBlob(article.text)
  for sentence in blob.sentences:
    for phrase in sentence.noun_phrases:
      news_db.insert_phrase(article.publish_date, phrase, sentence.polarity, 
                            article.url, article.url_root)

def _retry_url(news_db, url, url_root):
  article = newspaper.Article(url.strip())
  article.download()
  try:
    article.parse()
  except newspaper.article.ArticleException:
    print('Skipping %s after second attempt, due to ArticleException' %(url, ))
    return

  print('Retry was successful')
  article.url_root = url_root
  _consume_article(news_db, article)

def analyze_article(news_db, article):
  article.url = article.url.strip()
  if (news_db.article_is_in_db(article.url)):
    print("Skipping %s; already processed accoridng to db" %(article.url,))
    return

  article.download()
  try:
    article.parse()
  except newspaper.article.ArticleException:
    print('Trying %s again due to Article exception' %(article.url))
    _retry_url(news_db, article.url, article.url_root)
    return

  _consume_article(news_db, article)

def clean_tweet(t):
  t = re.sub(r'@[A-Za-z0-9]+', '', t) # remove @
  t = re.sub('https?://[A-Za-z0-9./]+', '', t) # remove urls
  return re.sub(r'#([\w_-]*)', 
            lambda m : ' '.join(wordninja.split(m.group(1))) +' ',
            t, flags=re.I) # replace hashtags with likely word parts

def analyze_tweet(twitter_db, analyzer, tweet):
  clean = clean_tweet(tweet.text)
  s = analyzer.polarity_scores(clean)

  from textblob import TextBlob # this is a hack
  blob = TextBlob(clean)
  for sentence in blob.sentences:
    for phrase in sentence.noun_phrases:
      twitter_db.insert_phrase(phrase, s['compound'], tweet)

def run(settings, queue, news_db, twitter_db):
  internet_analyzer = SentimentIntensityAnalyzer()
  try:
    while True:
      item = queue.get()

      if (type(item) is newspaper.article.Article):
        analyze_article(news_db, item)
      else: # TODO check for twitter object type
        analyze_tweet(twitter_db, internet_analyzer, item)
        pass

  finally:
    pass