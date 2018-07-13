# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from job.items import JobItem as Item
import datetime
from scrapy_redis.spiders import RedisCrawlSpider

class JobspiderSpider(RedisCrawlSpider):
    name = 'jobspider'
    allowed_domains = ['search.51job.com','jobs.51job.com']
    start_urls = [
        'https://search.51job.com/list/020000,000000,0000,00,9,99,java,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
        'https://search.51job.com/list/020000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
        'https://search.51job.com/list/020000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    ]

    def parse(self, response):
        # 当前时间字符串
        now_date_str = datetime.datetime.now().strftime("%m-%d")
        # 当前时间
        now_date = datetime.datetime.strptime(now_date_str, '%m-%d')
        '''
        发布日期小于三天就爬取
        '''
        xpath1 = "//div[@class='el']/span[@class='t5']/text()"
        pub_date_list = response.xpath(xpath1).extract()

        for i in range(len(pub_date_list)):

            # 发布的时间
            pub_date = datetime.datetime.strptime(pub_date_list[i], '%m-%d')

            if ((now_date - pub_date).days < 3):

                xpath = "//div[@class='el']/p[@class='t1 ']/span/a/@href"
                items = response.xpath(xpath)
                for index in range(len(items)):
                    yield Request(items[index].extract(), callback=self.parse_detail)

            '''
                下一页
            '''
        next_page_url = response.xpath("//*[@id='rtNext']/@href").extract_first()
        yield Request(next_page_url, callback=self.parse)

    def parse_detail(self, response):
        item = Item()
        item["title"] = response.xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/text()").extract_first()  # 获取细节标题
        item["location"] = response.xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]/span/text()").extract_first()
        item["url"] = str(response.url)
        item["salary"] = response.xpath("/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()").extract_first()
        item["date"] = response.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/div/span[4]/text()").extract_first()
        yield item
