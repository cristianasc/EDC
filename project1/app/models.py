from BaseXClient import BaseXClient


class Database:
    def __init__(self):

        self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        f = open('news_ua.xml', 'r', encoding='utf-8')

        try:
            # create new database
            self.session.create("database", f.read())
            print(self.session.info())

            # run query on database
            print("\n" + self.session.execute("xquery doc('database')"))

        finally:
            # close session
            if self.session:
                self.session.close()


    def add_new(self, new):

        print("here, the new " + new)
        # add new news
        add = "let $doc := collection('news')/channel " \
              "return insert node <newnode/> into $doc"

        query = self.session.execute(add)

        # close query object
        query.close()
