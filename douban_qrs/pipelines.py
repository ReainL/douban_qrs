# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging.config

from config import logger_path
from common.pgutils import get_conn, execute_select, execute_sql

logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")
conn = get_conn()


class DoubanQrsPipeline(object):
    def process_item(self, item, spider):
        return item


class crawlerDouban(object):
    def spider_Item(self, item, spider):
        try:
            with conn:
                sql_repeat = """
                    select * from public.db_movie where user_name=%s
                """
                print('piplines')
                res = execute_select(conn, sql_repeat, item['user_name'])
                if not res[0]:
                    sql_insert = """
                        INSERT INTO public.db_movie(user_name, comment_time, film_critics) 
                        VALUES(%s, %s, %s)
                    """
                    execute_sql(conn, sql_insert, item)
                    print('增加数据')
                else:
                    pass
        finally:
            if conn:
                conn.close()

