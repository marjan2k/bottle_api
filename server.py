import sqlite3
import bottle
import models
from gevent import monkey; monkey.patch_all()
from config import serverIP, serverPort, serverDebug, db


class server:
    def __init__(self):
        self.app = bottle
        self.conn = sqlite3.connect(db)
        self.routes()

    def start(self):
        self.dbInit()
        self.app.run(host=serverIP, port=serverPort, server="gevent", debug=serverDebug)

    def dbInit(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS users"
            "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name TEXT NOT NULL UNIQUE)")
        self.conn.commit()

    def routes(self):
        self.app.route('/', method="GET", callback=self.index)
        self.app.route('/new', method="POST", callback=self.new)

    def index(self):
        c=self.conn.cursor()
        c.execute("SELECT * FROM users;")
        results  = {c.fetchall()}
        return results

    def new(self):
        c=self.conn.cursor()
        name = self.app.request.forms.get("name")
        try:
            c.execute("INSERT INTO users (name)"
                      "VALUES (?)",
                      (name,))
            self.conn.commit()
            return {"SUCCESS"}
        except Exception as e:
            return {str(e)}

if __name__ == "__main__":
    app = server()
    app.start()
