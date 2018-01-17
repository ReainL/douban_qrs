# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanQrsItem(scrapy.Item):
    # 定义保存数据的名称
    user_name = scrapy.Field()     # 用户昵称
    comment_time = scrapy.Field()  # 发表时间
    film_critics = scrapy.Field()  # 影评
