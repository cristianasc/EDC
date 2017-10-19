from BaseXClient import BaseXClient
from urllib.parse import urlparse
import xmltodict

class Database:
    def __init__(self):

        self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        self.session.execute("open database")

    def add_new(self, new):
        self.session.execute("open database")
        self.session.execute("XQUERY insert node "+new+" into rss/channel")

    def news(self):
        news_txt = self.session.execute("XQUERY doc('database')")
        news = xmltodict.parse(news_txt)["rss"]["channel"]["item"]

        for i in range(0, len(news)):
            parsed_url = urlparse(news[i]['guid'])

            if bool(parsed_url.scheme):
                news[i]["uid"] = parsed_url.query
            else:
                news[i]["uid"] = "c="+news[i]['guid']

        return news

    def get_new(self, uid):
        new_txt = self.session.execute("XQUERY doc('database')//rss/channel/item[contains(guid, \""+str(uid)+"\")]")
        return dict(xmltodict.parse(new_txt)["item"])

    def validate_xml(self):
        self.session.execute("XQUERY let $schema:= 'news_ua.xsd' let $doc:= doc('database') return validate:xsd($doc, $schema)")

    def del_new(self, id):
        pass
