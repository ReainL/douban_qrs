#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-1-9

@author: Xu
"""
import jieba
import numpy as np
import matplotlib.pyplot as plt
import logging.config

from config import logger_path
from scipy.misc import imread
from snownlp import SnowNLP
from wordcloud import WordCloud, ImageColorGenerator
from common.pgutils import get_conn, execute_select


logging.config.fileConfig(logger_path)
logger = logging.getLogger("root")


def read_comment(conn):
    logger.info('读取数据库中数据...read_comment')
    film_critics = []
    sql_select = "SELECT * FROM db_movie"
    params = '100'
    result = execute_select(conn, sql_select)
    print(result)
    for res in result:
        logger.debug(res)
        comment = res[2]
        if comment:
            film_critics.append(comment)
    return film_critics


def word_cloud(comment):
    logger.info('制作词云图...word_cloud')
    comment_text = ''
    back_coloring = imread("static/zzb.jpg")
    cloud = WordCloud(font_path='static/simhei.ttf',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
                      background_color="white",  # 背景颜色
                      max_words=2000,  # 词云显示的最大词数
                      mask=back_coloring,  # 设置背景图片
                      max_font_size=100,  # 字体最大值
                      random_state=42,
                      width=360, height=591, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                      )
    for li in comment:
        comment_text += ' '.join(jieba.cut(li, cut_all=False))
    wc = cloud.generate(comment_text)
    image_colors = ImageColorGenerator(back_coloring)
    plt.figure("wordc")
    plt.imshow(wc.recolor(color_func=image_colors))
    wc.to_file('前任三词云图.png')


def snowlp_analysis(comment):
    logger.info('自然语言处理NLP...snow_analysis')
    sentimentslist = []
    for li in comment:
        s = SnowNLP(li)
        # logger.debug(li)
        # logger.debug(li, s.sentiments)
        print(li, s.sentiments)
        sentimentslist.append(s.sentiments)
    fig1 = plt.figure("sentiment")
    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.02))
    plt.show()


if __name__ == '__main__':
    conn = None
    try:
        conn = get_conn()
        with conn:
            comment_list = read_comment(conn)
            word_cloud(comment_list)
            snowlp_analysis(comment_list)
    finally:
        if conn:
            conn.close()
