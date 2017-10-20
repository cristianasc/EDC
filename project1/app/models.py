from BaseXClient import BaseXClient
from urllib.parse import urlparse
import xmltodict
from collections import OrderedDict


class Database:
    def __init__(self):

        self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        self.session.execute("open database")
        self.session.execute("open likes")
        self.session.execute("open comments")

    def add_new(self, new, new_uid):
        self.session.execute("open database")
        self.session.execute("XQUERY insert node "+new+" into rss/channel")

        self.session.execute("open likes")
        self.session.execute("XQUERY insert node <new/> into likes")
        self.session.execute("XQUERY insert node attribute newattr {'"+str(new_uid)+"'} into likes/new[1]")
        self.session.execute("XQUERY insert node <like/> into likes/new[1]")
        self.session.execute("XQUERY replace value of node likes/new[1]/like[1] with '0'")
        self.session.execute("XQUERY insert node <dislike/> into likes/new[1]")
        self.session.execute("XQUERY replace value of node likes/new[1]/dislike[1] with '0'")
        self.session.execute("XQUERY insert node <userid/> into likes/new[1]")


        self.session.close()

    def news(self):
        news_txt = self.session.execute("XQUERY doc('database')")
        news = xmltodict.parse(news_txt)

        if "rss" in news and "channel" in news["rss"] and "item" in news["rss"]["channel"]:
            news = news["rss"]["channel"]["item"]
            if type(news) is OrderedDict:
                news = [news]
        else:
            return []

        for i in range(0, len(news)):
            parsed_url = urlparse(news[i]['guid'])

            if bool(parsed_url.scheme):
                news[i]["guid"] = parsed_url.query.replace("c=","")

        return news

    def get_new(self, uid):
        new_txt = self.session.execute("XQUERY doc('database')//rss/channel/item[contains(guid, \""+str(uid)+"\")]")
        return dict(xmltodict.parse(new_txt)["item"])

    def validate_xml(self):
        self.session.execute("XQUERY let $schema:= 'news_ua.xsd' let $doc:= doc('database') return validate:xsd($doc, $schema)")

    def del_new(self, uid):
        self.session.execute("XQUERY let $doc:= doc('database') return delete node $doc//rss/channel//item[contains(guid, \"" + str(uid) + "\")]")

    def like(self, uid, value, guid):
        print("OLAA")
        print(guid)
        #self.session.execute("XQUERY doc('likes') insert node <new>"+str(guid)+"</new> into likes")
        pass

    def dislike(self, uid, value):
        pass

    def comment(self, uid, comment):
        pass
