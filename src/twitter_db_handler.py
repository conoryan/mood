from db_handler import DBHandler

class TwitterDBHandler(DBHandler):
  def __init__(self, filename, table_name):
    DBHandler.__init__(self, filename, table_name)

    c = self._get_cursor()
    c.execute("SELECT * FROM sqlite_master WHERE name = ?", (self._table_name, ))
    if (len(c.fetchall()) == 0):
      c.execute('CREATE TABLE {tn} (id INTEGER PRIMARY KEY, '
          'datetime TEXT, phrase TEXT, sentiment REAL, likes INTEGER, '
          'retweets INTEGER, user_id INTEGER)'.format(tn=self._table_name))

    self._conn.commit()

  def insert_phrase(self, phrase, polarity, src_tweet):
    c = self._get_cursor()
    c.execute("INSERT INTO {tn} (id, datetime, phrase, sentiment, likes, "
              "rewtweets, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
                .format(tn=self._table_name)
              , (str(src_tweet.id), str(src_tweet.created_at), phrase, 
                 str(polarity), str(src_tweet.favorite_count), 
                 str(src_tweet.retweet_count), str(src_tweet.user.id))
              )
    self._conn.commit()

  # finds CONTAINING phrase, not strict match
  # date start and end are both inclusive
  # return entries as (sentiment, likes, retweets)
  def get_data_for_phrase(self, phrase, start_date, end_date):
    c = self._get_cursor()
    print('%'+phrase+'%')
    c.execute("SELECT sentiment, likes, retweets FROM '{tn}' WHERE phrase "
              "LIKE ? AND datetime BETWEEN ? AND ?".format(tn=self._table_name), 
              ('%'+phrase+'%', str(start_date), str(end_date)))

    return c.fetchall()