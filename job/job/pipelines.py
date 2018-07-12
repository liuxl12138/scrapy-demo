# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class JobPipeline(object):
    def process_item(self, item, spider):
      pass


class ScrapyMYSQLPipeline(object):
    def open_spider(self, spider):
        self.connect = pymysql.Connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            db="jobcrawler",
            charset="utf8"
        )
        self.cursor = self.connect.cursor()
        pass

    def process_item(self, item, spider):

        sql = "insert into job(title,location,url,salary,date) values('%s','%s','%s','%s','%s')"
        self.cursor.execute(sql % (item["title"], item["location"], item["url"], item["salary"], item["date"]))
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
        pass
