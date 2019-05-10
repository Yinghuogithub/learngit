#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#my aiohttp test
async def create_pool(loop,**kw)
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host','localhost'),
        port=kw.get('port',3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf-8'),
        autocommit=kw.get('autocommit',True)
        maxsize=kw.get()
    
    
    )