# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

from itemadapter import ItemAdapter
import pymysql


class JingdongPipeline:
    # def __init__(self):
    #     header = ('评论人数', '商品链接', '价格', '商店链接', '商店名称', '标题')
    #     self.file = open('jd.csv', 'w', newline='')
    #     self.csvwriter = csv.writer(self.file)
    #     self.csvwriter.writerow(header)
    #
    # def process_item(self, item, spider):
    #     self.csvwriter.writerow(
    #         [item['comment'], item['phone_link'], item['price'], item['stone_link'], item['stone_name'], item['title']])
    #     return item
    #
    # def close_spider(self, spider):
    #     self.file.close()
    def __init__(self):
        #     开启链接数据库
        self.db = pymysql.connect(host="localhost", port=3306, user="root", password="baidu123", database="jingdong")
        self.curos = self.db.cursor()

    def process_item(self, item):
        # print(item)
        print("数据存储！！！！！！！！！！！！！")
        # 调用数据储存函数
        sql = "insert into jd(comment,phone_link,price,stone_link,stone_name,title) values ('%s','%s','%s','%s','%s','%s')" \
              % (
                  item['comment'], item['phone_link'], item['price'], item['stone_link'], item['stone_name'],
                  item['title'])
        self.curos.execute(sql)
        self.db.commit()
        return item

    def __del__(self):
        self.curos.close()
        self.db.close()
