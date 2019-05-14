#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#app.py for awesome_sp project

import logging;logging.basicConfig(level=logging.INFO)

import asyncio,os,json,time
from datetime import datetime

from aiohttp import web

def index(request):
    return web.Response(body='<h1>Welcome to my web...</h1>'.encode('utf-8'),content_type='text/html')
    #return web.Response(body='<h1>Welcome to my web...</h1>'.encode('utf-8'),content_type='text/html')

def init():
    app = web.Application()
    app.router.add_route('GET','/',index)
    web.run_app(app,host='127.0.0.1',port=9000)
    #srv = await loop.create_server(app.make_handler(),'127.0.0.1',9000)
    logging.info('server started at http://127.0.0.1:9000...')
    web.run_app(app,host='127.0.0.1',port=9000)
    #return srv 

init()

#this is a test for vscode and git

