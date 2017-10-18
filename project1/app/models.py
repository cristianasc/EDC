from BaseXClient import BaseXClient
from xml.etree.ElementTree import ElementTree, tostring
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import json
import xmltodict


class Database:
    def __init__(self):

        self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        f = open('news_ua.xml', 'r', encoding='utf-8')

        self.session.execute("open database")

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
        self.session.execute("XQUERY insert node "+new+" into rss/channel")

    def news(self):
        news_txt = self.session.execute("XQUERY doc('database')")
        news = xmltodict.parse(news_txt)["rss"]["channel"]["item"]

        for i in range(0, len(news)):
            news[i]["uid"] = urlparse(news[i]['guid']).query

        return news

    def get_new(self, uid):
        new_txt = self.session.execute("XQUERY doc('database')//rss/channel/item[guid=\"https://uaonline.ua.pt/pub/detail.asp?c="+uid+"\"]")
        return dict(xmltodict.parse(new_txt)["item"])






