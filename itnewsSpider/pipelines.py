# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json


class DuplicatesPipeline:
    """IT新闻标题去重"""
    def __init__(self):
        self.title_seen = set()

    def process_item(self, item, spider):
        if item['title'] in self.title_seen:
            raise DropItem("Duplicate news title found: %s" % item)
        else:
            self.title_seen.add(item['title'])
        return item


class ItnewsspiderPipeline(object):

    def __init__(self):
        self.json_file = open('solidot_news.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.json_file.write(line.encode('utf-8').decode('unicode-escape'))
        return item
