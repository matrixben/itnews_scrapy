# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json
import psycopg2


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


class PostgresPipeline:
    def __init__(self, hostname, dbname, username, password, port):
        """连接数据库"""
        self.hostname = hostname
        self.dbname = dbname
        self.username = username
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            hostname=crawler.settings.get('POSTGRESQL_HOST'),
            dbname=crawler.settings.get('POSTGRESQL_DB'),
            username=crawler.settings.get('POSTGRESQL_USER'),
            password=crawler.settings.get('POSTGRESQL_PWD'),
            port=crawler.settings.get('POSTGRESQL_PORT')
        )

    def open_spider(self, spider):
        self.conn = psycopg2.connect(host=self.hostname, database=self.dbname, user=self.username,
                                     password=self.password, port=self.port)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # 检查是否已存入数据库
        if self.select_news(item):
            raise DropItem("Duplicate news title found: %s" % item)

        insert_news_sql = "insert into news(title,tag,publish_date,source_url) values(%s,%s,%s,%s)"
        values = (item['title'], item['tag'], item['publish_date'], item['source_url'])
        self.cur.execute(insert_news_sql, values)
        self.conn.commit()
        return item

    def select_news(self, item):
        print(item['title'])
        select_news_sql = "select title from news where title = %s"
        self.cur.execute(select_news_sql, (item['title'],))
        exist_title = self.cur.fetchone()
        if exist_title:
            return exist_title[0]
        return ''
