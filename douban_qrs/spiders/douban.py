# -*- coding: utf-8 -*-
import scrapy
import urllib
import logging.config
import random

from settings import user_agent_list
from config import logger_path
from douban_qrs.items import DoubanQrsItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")


# 自定义的爬虫程序处理类，要继承scrapy模块的spider类型
class DoubanSpider(scrapy.Spider):
    name = 'douban'  # 定义爬虫程序的名称，用于程序的启动使用
    allowed_domains = ['https://movie.douban.com']  # 定义爬虫程序运行的作用域--域名
    headers = random.choice(user_agent_list)

    def start_requests(self):
        return [scrapy.Request("https://accounts.douban.com/login",
                callback=self.logged_in,
                meta={
                    "cookiejar": 1
                }
                )]

    def logged_in(self, response):
        img_code = response.xpath("//img[@id='captcha_image']/@src").extract()
        if len(img_code) > 0:
            print("请输入验证码登录")
            localpath = "/home/xsl/imgcode.jpg"
            # 将图片下载到本地
            urllib.request.urlretrieve(img_code[0], filename=localpath)
            print("请查看本地验证码图片并输入验证码")
            img_code_value = input()
            data = {
                "form_email": "你的账号",
                "form_password": "您的密码",
                "captcha-solution": str(img_code_value),
            }

        else:
            print("此时没有验证码")
            data = {
                "form_email": "你的账号",
                "form_password": "您的密码",
            }
        print("登录中.(ง •̀_•́)ง")
        return [scrapy.FormRequest('https://www.douban.com/login',
                                   formdata=data,
                                   callback=self.movie)]

    def movie(self, response):
        yield scrapy.Request('https://movie.douban.com/subject/26662193/comments', callback=self.parse)

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
            next_page = '//div[@id = "paginator"]/a[@class="next"]/@href'
            if response.xpath(next_page):
                url_nextpage = 'https://movie.douban.com/subject/26662193/comments' + response.xpath(next_page).extract()[0]
                request = scrapy.Request(url_nextpage, callback=self.parse)
                yield request
