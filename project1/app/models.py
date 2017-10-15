from BaseXClient import BaseXClient


class Database:

    def __init__(self):

        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        f = open('news_ua.xml', 'r', encoding='utf-8')

        try:
            # create new database
            session.create("database", f.read())
            print(session.info())

            # run query on database
            print("\n" + session.execute("xquery doc('database')"))

        finally:
            # close session
            if session:
                session.close()
