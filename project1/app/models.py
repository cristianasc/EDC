from BaseXClient import BaseXClient


class Database:
    def __init__(self):

        self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        f = open('news_ua.xml', 'r', encoding='utf-8')

        try:
            # create new database
            self.session.create("database", f.read())
            print(self.session.info())

            self.session.execute("xquery drop db ('database')")
            # run query on database
            self.session.execute("xquery doc('database')")

        finally:
            # close session
            pass


    def add_new(self, new):

        add = "XQUERY insert node "+new+" into rss/channel"

        query = self.session.execute(add)
        print(query)

