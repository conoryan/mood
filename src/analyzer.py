import sqlite3

def parse_settings(settings):
  db_location = settings['DataBase']

  return db_location

def analyze_sentence(c, sentence, datetime, url):
  for phrase in sentence.noun_phrases:
    c.execute("INSERT INTO phrases (datetime, phrase, sentiment, url) VALUES (?, ?, ?, ?)" \
              , (str(datetime), phrase, str(sentence.polarity), url))

def analyze(c, article):
  from textblob import TextBlob # this is a hack
  blob = TextBlob(article.text)

  for sentence in blob.sentences:
    analyze_sentence(c, sentence, article.publish_date, article.url)

def init_db(db_location):
  conn = sqlite3.connect(db_location)
  c = conn.cursor()

  c.execute("SELECT * FROM sqlite_master WHERE name = 'phrases'") # exists
  if (len(c.fetchall()) == 0):
    c.execute('CREATE TABLE phrases (id INTEGER PRIMARY KEY, datetime TEXT, phrase TEXT, '
              'sentiment REAL, url TEXT)')
  conn.commit()

  return c, conn

def run(settings, queue):
  db_location = parse_settings(settings)
  c, conn = init_db(db_location)

  try:
    while True:
      item = queue.get()
      item.download()
      item.parse()

      analyze(c, item)
      conn.commit()
  finally:
    conn.close()