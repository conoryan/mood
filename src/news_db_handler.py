from db_handler import DBHandler

class NewsDBHandler(DBHandler):
  def __init__(self, filename, table_name):
    DBHandler.__init__(self, filename, table_name)

    c = self._get_cursor()
    c.execute("SELECT * FROM sqlite_master WHERE name = ?", (self._table_name, ))
    if (len(c.fetchall()) == 0):
      c.execute('CREATE TABLE {tn} (id INTEGER PRIMARY KEY, '
          'datetime TEXT, phrase TEXT, sentiment REAL, url TEXT)'
            .format(tn=self._table_name))

    self._conn.commit()

  def insert_phrase(self, date, phrase, polarity, url):
    c = self._get_cursor()
    c.execute("INSERT INTO {tn} (datetime, phrase, sentiment, url) VALUES (?, ?, ?, ?)"
                .format(tn=self._table_name)
              , (str(date), phrase, str(polarity), url))
    self._conn.commit()

  # finds CONTAINING phrase, not strict match
  def get_scores_for_phrase(self, phrase):
    c = self._get_cursor()
    print('%'+phrase+'%')
    c.execute("SELECT ({get}) FROM '{tn}' WHERE {filter} LIKE ?".format(
        get='sentiment', tn=self._table_name, filter='phrase'), 
        ('%'+phrase+'%', ))
    scores = c.fetchall()
    print(scores)