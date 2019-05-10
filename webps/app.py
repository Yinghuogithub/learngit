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

#创建连接池
async def creat_pool(loop,**kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host','localhost'),
        port=kw.get('port',3306),
        user=kw['user'],
        password=kw['password'],
        bd=kw['db'],
        charset=kw.get('charset','utf8'),
        autocommit=kw.get('autcommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.get('minsize',1)
        loop=loop
    )
    
#Select
async def select(sql,args,size=None):
    log(sql,args)
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?','%s'), args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info('rows returned:%s' % len(rs))
        return rs
        
#define execute to run INSERT UPDATE DELETE
async def execute(sql,args):
    log(sql)
    with(await __pool) as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?','%s'),args)
            affected = cur.rowcount
            await cur.close()
        except BaseException as e:
            raise
        return affected
        
#ORM
from orm import Model, StringField, IntegerField

class User(Model):
    __table__ = 'uses'
    
    id = IntegerField(primary_key=True)
    name = StringField()
    
#创建实例
user = User(id=123,name='Yinghuo')
#存入数据库
user.insert()
#查询所有User对象
users = User.findALL()

#定义Model
#首先定义的是所有ORM映射的基类Model
class Model(dict,metaclass=ModelMetaclass):
    
    def __init__(self,**kw):
        super(Model,self).__init__(**kw)
        
    def __getattr__(self,key):
        try:
            return self[key]
        except KeyError:
            raise AttrbuteError(r"'Model' object has no attrbute '%s'"%key)
            
    def __setattr__(self,key,value):
        self[key] = value
        
    def getValue(self,key,value):
        self[key]=value
        
    def getValueOrDefault(self,key):
        value = getattr(self,key,None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' %(key,str(value)))
                setattr(self,key,value)
        return value
        
class Field(object):
    def __init__(self,name,column_type,primary_key,default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default
        
    def __str__(self):
        return '<%s,%s:%s>' %(self.__class__.__name__,self.column_type,self.name)
        
#映射varchar的StringField
class StringField(Field):
    
    def __init__(self,name=None,primary_key=False,default=None,ddl='varchar(100)'):
        super().__init__(name,ddl,primary_key,default)
        
#注意到Model只是一个基类，将具体的子类如User的映射信息读取出来
class ModelMetaclass(type):
    
    def __new__(cls,name,bases,attrs):
    #排除Model类本身
    if name=='Model':
        return type.__new__(cls,name,bases,attrs)
    #获取table名称：
    tableName = attrs.get('__table__',None) or name
    logging,info('found model: %s (table:%s)' %(name,tableName))
    #获取所有的Field和主键名:
    mappinga = dict()
    field = []
    primaryKey = None
    for k,v in attrs.items():
        if isinstance(v,Field):
            logging.info('  found mapping:%s ==> %s'%(k,v))
            mapping[k] = v
            if v.primary_key:
                #找到主键：
                if primaryKey:
                    raise RuntimeError('Duplicate primary key for field:%s' %k)
                
                primary = k
                else:
                    fields.append(k)
    if not primaryKey:
        raise RuntimeError('Primary key not found.')
    for k in mappings.key():
        attrs.pop(k)
    escaped_fields = list(map(lambda f: '`%s`'%f,fields))
    attrs['__mappings__'] = mappings  #保存属性和列的映射关系
    attrs['__table__'] = tableName
    attrs['__primary_key__'] = primaryKey  #主键属性名
    attrs['__fields__'] = fields  #除主键外的属性名
    #构造默认的SELECT,INSERT,UPDATE,DELETE语句
    attrs['__select__'] = 'select `%s`,%s from `%s`' %(primaryKey,','.join(escaped_fields),tableName)
    attrs['__insert__'] = 'insert into `%s` (%s,`%s`) values (%s)' % (tableName,','.join(escaped_fields),primaryKey,create_args_string(len(escaped_fields)+1))
    attrs['__update__'] = 'update `%s` set %s where `%s`=?'%(tableName,',',join(map(lambda f: '`%s`=?'%(mappings.get(f).name or f),fields)),primaryKey)
    attrs['__delete__'] = 'delete from `%s` where `%s`=?'%(tableName,primaryKey)
    return type.__new__(cls,name,bases,sttrs)




