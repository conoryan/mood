from db_handler import DBHandler

class NewsDBHandler(DBHandler):
  def __init__(self, filename, table_name):
    DBHandler.__init__(self, filename, table_name)

    c = self._get_cursor()
    c.execute("SELECT * FROM sqlite_master WHERE name = ?", (self._table_name, ))
    if (len(c.fetchall()) == 0):
      c.execute('CREATE TABLE {tn} (id INTEGER PRIMARY KEY, '
          'datetime TEXT, phrase TEXT, sentiment REAL, url TEXT, url_root TEXT)'
            .format(tn=self._table_name))

    self._conn.commit()

  def insert_phrase(self, date, phrase, polarity, url, url_root):
    c = self._get_cursor()
    c.execute("INSERT INTO {tn} (datetime, phrase, sentiment, url, url_root) "
              "VALUES (?, ?, ?, ?, ?)".format(tn=self._table_name)
              , (str(date), phrase, str(polarity), url, url_root))
    self._conn.commit()

  # finds CONTAINING phrase, not strict match
  # date range is INCLUSIVE on both ends.
  # returns entries as (sentiment, url_root) -> url_root is as in SourcesFile
  # datetime.strptime("2017-08-18 00:00:00", "%Y-%m-%d %H:%M:%S")
  def get_data_for_phrase(self, phrase, start_date, end_date):
    c = self._get_cursor()
    c.execute("SELECT sentiment, url_root FROM '{tn}' WHERE phrase LIKE ? "
              "AND datetime BETWEEN ? AND ?".format(tn=self._table_name), 
              ('%'+phrase+'%', str(start_date), str(end_date)))

    return c.fetchall()

  # given a url to an article, returns true if that url is in db already
  # use before processing a new article to confirm article is not being reprocessed
  def article_is_in_db(self, url):
    c = self._get_cursor()
    c.execute("SELECT (sentiment) FROM '{tn}' WHERE url IS ? "
              .format(tn=self._table_name), 
              (url, ))

    return (len(c.fetchall()) > 0)
