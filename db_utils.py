import sqlite3

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect('flask.db')
    rv.row_factory = dict_factory
    return rv

def get_db(g):
    """Opens a new database connection if there is none
       yet for the current application context. """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def close_db(error, g):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def dict_factory(cur, row):
    d = {}
    for i, col in enumerate(cur.description):
        d[col[0]] = row[i]
    return d

