import re

import jsonpath
import requests
import scrapy

from ..items import JingdongItem
# //*[@id="J_goodsList"]
# //*[@id="J_goodsList"]/ul/li[1]/div/div[4]/a/em
# //*[@id="J_goodsList"]/ul/li[2]/div/div[4]
# //*[@id="J_goodsList"]/ul/li[3]/div/div[4]

class JingdongSpider1Spider(scrapy.Spider):
    name = "jingdong_spider1"
    allowed_domains = ["jd.com"]
    page = int(input("请输入爬取页面"))
    url = "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&wq=%E6%89%8B%E6%9C%BA&pvid=8858151673f941e9b1a4d2c7214b2b52&page={}&s=1&click=0"
    end_page = 0
    start_urls = [url.format(end_page)]

    def parse(self, response):
        li_list = response.xpath('//*[@id="J_goodsList"]/ul/li')
        for li in li_list:
            title = li.xpath('./div/div[4]/a/em/text()').extract()
            price = li.xpath('./div/div[3]/strong/i/text()').extract()

            phone_link = li.xpath('./div/div[4]/a/@href').extract()
            stone_name = li.xpath('./div/div[7]/span/a/text()').extract()
            stone_link = li.xpath('./div/div[7]/span/a/@href').extract()

            for i in phone_link:
                link = re.findall('com/(.*?).h.*?', i)
                link = ''.join(link)

                url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productCommentSummaries&client=pc&clientVersion=1.0.0&t=1685450991315&referenceIds={}' \
                      '&categoryIds=9987%2C653%2C655&loginType=3&bbtf=&shield=&uuid=122270672.812679033.1674991323.1674991323.168544943'.format(
                    link)
                # print(url)
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
                }
                json_data = requests.get(url=url, headers=headers).json()
                comment = jsonpath.jsonpath(json_data, '$..CommentCountStr')
            # print(comment)
            item = JingdongItem()
            item['title'] = title[0]
            item['price'] = price[0]
            item['comment'] = comment[0]
            item['phone_link'] = phone_link[0]
            item['stone_name'] = stone_name[0]
            item['stone_link'] = stone_link[0]
            print(item)
            yield item
            # yield scrapy.Request(self.url.format(self.page), callback=self.parse)

        if self.page <= 98:

            if self.page == 1:
                self.new_page = 1

            else:
                self.new_page = (self.page * 2) - 1
                yield scrapy.Request(self.url.format(self.new_page), callback=self.parse)
                print("第" + self.page + "页")
