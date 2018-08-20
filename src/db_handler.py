import sqlite3

class DBHandler:
  def _get_cursor(self):
    return self._conn.cursor()

  def __init__(self, filename, table_name):
    self._filename    = filename
    self._conn        = sqlite3.connect(self._filename)
    self._table_name  = table_name
