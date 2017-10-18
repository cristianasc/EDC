from BaseXClient import BaseXClient
from xml.etree.ElementTree import ElementTree, tostring
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import json


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
        self.session.execute("XQUERY insert node "+new+" into rss/channel")

    def news(self):
        news = {}
        titles = []
        descriptions = []
        guid = []
        i = 1

        count = self.session.execute("XQUERY let $items:=doc('database')//channel/item/title[1]/text() return count($items)")

        self.session.execute("open database")

        while(i<=int(count)):
            titles += [self.session.execute("XQUERY (for $i in doc('database')//channel/item/title/text() return $i)["+str(i)+"]")]
            descriptions += [self.session.execute("XQUERY (for $i in doc('database')/rss/channel/item/description/text() return $i)["+str(i)+"]")]
            guid += [self.session.execute("XQUERY (for $i in doc('database')/rss/channel/item/guid/text() return $i)["+str(i)+"]")]
            i = i + 1

        for i,j in zip(titles,descriptions):
            news[i] = [j]

        return news, guid






