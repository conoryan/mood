import sqlite3

class DBHandler:
  def _get_cursor(self):
    return self._conn.cursor()

  def __init__(self, filename, table_name):
    self._filename    = filename
    self._conn        = sqlite3.connect(self._filename)
    self._table_name  = table_name

    c = self._get_cursor()
    c.execute("SELECT * FROM sqlite_master WHERE name = ?", (self._table_name, ))
    if (len(c.fetchall()) == 0):
      c.execute('CREATE TABLE phrases (id INTEGER PRIMARY KEY, '
          'datetime TEXT, phrase TEXT, sentiment REAL, url TEXT)')

    self._conn.commit()

  def insert_phrase(self, date, phrase, polarity, url):
    c = self._get_cursor()
    c.execute("INSERT INTO phrases (datetime, phrase, sentiment, url) VALUES (?, ?, ?, ?)"
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