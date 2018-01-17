# -*- coding: utf-8 -*-
import scrapy
import logging.config

from config import logger_path
from douban_qrs.items import DoubanQrsItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")


# 自定义的爬虫程序处理类，要继承scrapy模块的spider类型
class DoubanSpider(scrapy.Spider):
    name = 'douban1'  # 定义爬虫程序的名称，用于程序的启动使用
    allowed_domains = ['https://movie.douban.com']  # 定义爬虫程序运行的作用域--域名
    # 定义爬虫程序真实爬取url地址的列表/原组 两种方法
    # 第一种方法是我们使用代码增加每页的参数
    # def start_requests(self):
    #     start = 20
    #     for i in range(1, 2375):
    #         url = 'https://movie.douban.com/subject/26662193/comments?start=' + str(start) + '&limit=20&sort=new_score&status=P&percent_type=/'
    #         start += 20
    #         # Request 是Scrapy发送Get请求的方法
    #         yield scrapy.Request(
    #             url=url,
    #             callback=self.parse
    #         )

    # 第二种使用Scrapy的深度爬虫,设置提取规则(个人推荐使用第二种)
    # start_urls = [
    #     'https://movie.douban.com/subject/26662193/comments?start=0&limit=20&sort=new_score&status=P&percent_type=', ]
    # # 定义提取链接的规则
    # print('111111111112222221')
    # page_link = LinkExtractor(allow=('comments?start=\d+'))
    # print('11111111111')
    # # 定义爬取数据的规则
    # rules = {
    #     Rule(page_link, callback='parse', follow=True)
    # }
    def start_requests(self):
        cookies = {
            "bid": "kdAT04llDLQ",
            "ll": "108296",
            "ap": 1,
            "_pk_ref.100001.4cf6": "%5B%22%22%2C%22%22%2C1516156227%2C%22http%3A%2F%2Fwww.jianshu.com%2Fwriter%22%5D",
            "ps": "y",
            "dbcl2": "172701399:q0uOHWWHiGg",
            "ck": "b5AH",
            "__utma": "30149280.477977132.1510553147.1516150928.1516156326.13",
            "__utmb": "30149280.0.10.1516156326",
            "__utmc": 30149280,
            "__utmz": "30149280.1516156326.13.13.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/phone/bind",
            "__utmt": 1,
            "__utma": "223695111.1055290440.1515822378.1515979903.1516156326.3",
            "__utmb": "223695111.1.10.1516156326",
            "__utmc": "223695111",
            "__utmz": "223695111.1516156326.3.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/phone/bind",
            "_pk_id.100001.4cf6": "0052f64283dc106d.1515822378.3.1516156326.1515979903.",
            "_pk_ses.100001.4cf6": "*",
            "push_noty_num": 0,
            "push_doumail_num": 0
        }
        start = 20
        for i in range(1, 250):
            url = 'https://movie.douban.com/subject/26662193/comments?start=' + str(start) + '&limit=20&sort=new_score&status=P&percent_type=/'
            start += 20
        return [scrapy.Request(url=url, cookies=cookies, callback=self.parse)]

    def parse(self, response):
        item = DoubanQrsItem()
        html = response.xpath('//*[@id="comments"]')
        print(html)
        # all_data = html.find_all('div', class_='comment-item')
        for all_data in html:
            data = all_data.xpath('//*[@id="comments"]/div[@class="comment-item"]')
            item['user_name'] = data.xpath('/div[@class="comment"]/h3/span[@class="comment-info"]/a/text()')
            item['comment_time'] = data.xpath('//span[@class="comment-time"]/text()').strip().replace('\n', '')
            item['film_critics'] = data.xpath('/div[@class="comment"]/h3/p/text()').strip().replace('\n', '')
            logger.debug(item)
            print(item)
            yield item



