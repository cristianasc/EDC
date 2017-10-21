from BaseXClient import BaseXClient
from urllib.parse import urlparse
import xmltodict
from collections import OrderedDict


class Database:
    def __init__(self):
        self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    def add_new(self, new, new_uid):
        self.session.execute("open database")
        self.session.execute("XQUERY insert node "+new+" into rss/channel")

        self.session.execute("open likes")
        self.session.execute("XQUERY insert node <new/> before likes/new[1]")
        self.session.execute("XQUERY insert node attribute id {'"+str(new_uid)+"'} into likes/new[1]")
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

        return news

    def get_new(self, uid):
        new_txt = self.session.execute("XQUERY doc('database')//rss/channel/item[contains(guid, \""+str(uid)+"\")]")
        return dict(xmltodict.parse(new_txt)["item"])

    def get_likes(self, uid):
        likes = self.session.execute("XQUERY doc('likes')/likes/new[contains(@id, '" + str(uid) + "')]/like[1]/text()")
        dislikes = self.session.execute("XQUERY doc('likes')/likes/new[contains(@id, '" + str(uid) + "')]/dislike[1]/text()")
        return likes, dislikes

    def validate_xml(self):
        self.session.execute("XQUERY let $schema:= 'news_ua.xsd' let $doc:= doc('database') return validate:xsd($doc, $schema)")
        self.session.execute("XQUERY let $schema:= 'likes.xsd' let $doc:= doc('likes') return validate:xsd($doc, $schema)")
        self.session.execute("XQUERY let $schema:= 'comments.xsd' let $doc:= doc('comments') return validate:xsd($doc, $schema)")

    def del_new(self, uid):
        self.session.execute("XQUERY let $doc:= doc('database') return delete node $doc//rss/channel//item[contains(guid, \"" + str(uid) + "\")]")
        self.session.execute("XQUERY let $doc:= doc('comments') return delete node $doc/comments/comment[contains(new_id, '" + str(uid) + "')]")
        self.session.execute("XQUERY let $doc:= doc('likes') return delete node $doc/likes/new[contains(@id, '" + str(uid) + "')]")

    def like(self, uid, value, guid):
        self.session.execute("XQUERY replace value of node doc('likes')/likes/new[contains(@id, '" + guid + "')]/like[1] with '"+value+"'")
        self.session.execute("XQUERY replace value of node doc('likes')/likes/new[contains(@id, '" + guid + "')]/userid[1] with '"+uid+"'")

    def dislike(self, uid, value, guid):
        self.session.execute("XQUERY replace value of node doc('likes')/likes/new[contains(@id, '" + guid + "')]/dislike[1] with '" + value + "'")
        self.session.execute("XQUERY replace value of node doc('likes')/likes/new[contains(@id, '" + guid + "')]/userid[1] with '" + uid + "'")

    def comment(self, uid, name, comment, new_id):
        self.session.execute("open comments")
        self.session.execute("XQUERY insert node <comment>"
                              "<new_id>"+new_id+"</new_id>"
                              "<profile_uid>"+uid+"</profile_uid>"
                              "<profile_name>"+name+"</profile_name>"
                              "<text>"+comment+"</text>"
                              "</comment> into comments")

    def get_comments(self, new_id):
        try:
            comments = self.session.execute("XQUERY doc('comments')/comments/comment[contains(new_id, '" + new_id + "')]")
            comments = xmltodict.parse("<comments>"+comments+"</comments>")["comments"]["comment"]

            if type(comments) is OrderedDict:
                comments = [comments]

            return comments
        except TypeError:
            return []

    def get_favorites(self, limit):
        i=1
        top_news={}
        query = self.session.execute("XQUERY for $b in doc('likes')//likes/new order by $b/like descending where $b/like > 0 return $b")

        if query == "":
            return []

        news = xmltodict.parse("<new>"+query+"</new>")["new"]["new"]

        if type(news) is OrderedDict:
            news = [news]

        for new in news:
            if i <= limit:
                top_news[str(i)] = new["@id"]
                i += 1

        return top_news