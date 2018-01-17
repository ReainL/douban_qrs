#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-1-17

@author: Xu
"""
import psycopg2
import settings


def get_conn():
    host = settings.host
    database = settings.database
    user = settings.user
    password = settings.password
    port = 5432
    try:
        conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    except Exception as e:
        raise Exception("连接数据库出错：%s", repr(e))
    return conn


def execute_select(conn, sql, params=None):
    with conn.cursor() as cur:
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        return cur.fetchall()


def execute_sql(conn, sql, params=None):
    with conn.cursor() as cur:
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)