from BaseXClient import BaseXClient


class Database:
    def __init__(self):

        self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        f = open('news_ua.xml', 'r', encoding='utf-8')

        try:
            # create new database
            #self.session.create("database", f.read())
            print(self.session.info())

            # run query on database
            self.session.execute("xquery doc('database')")

        finally:
            # close session
            pass


    def add_new(self, new):

        self.session.execute("open database")
        query = self.session.execute("XQUERY insert node "+new+" into rss/channel")
        print(query)

