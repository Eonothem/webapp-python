#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Eonothem'

import asyncio, logging

import aiomysql

def log(sql, args=()):
	logging.info('SQL: %s' % sql)

@asyncio.coroutine
def create_pool(loop, **kw):#to create a database connection pool
	logging.info('create database connection pool...')
	global __pool#use global variable to save the connections
	__pool = yield from aiomysql.create_pool(
		host=kw.get('host', 'localhost'),
		port=kw.get('port', 3306),
		user=kw['user'],
		password=kw['password'],
		db=kw['db'],
		charset=kw.get('charset', 'utf-8'),
		autocommit=kw.get('autocommit', True),
		maxsize=kw.get('maxsize', 10),
		minsize=kw.get('minsize', 1),
		loop=loop
	)

@asyncio.coroutine
def select(sql, args, size=None):#to execute the 'select' command
	log(sql, args)
	global __pool

	with(yield from __pool) as conn:
		cur = yield from conn.cursor(aiomysql.DictCursor)
		yield from cur.execute(sql.replace('?', '%s'), args or ())

		if size:
			rs = yield from cur.fetchmany(size)
		else:
			rs = yield from cur.fetchall()

		yield from cur.close()
		logging.info('rows returned: %s' % len(rs))
		return rs

@asyncio.coroutine
def execute(sql, args):#to execute the 'insert', 'update' and 'delete' commands
	log(sql, args)

	with(yield from __pool) as conn:
		try:
			cur = yield from conn.cursor()
			yield from cur.execute(sql.replace('?', '%s'), args)
			affected = cur.rowcount#the count of result affected
			yield from cur.close()
		except BaseException as e:
			raise
		return affected

class Field(object):#define field class to save the name and type in the database

	def __init__(self, name, column_type, primary_key, default):
		self.name = name 
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default

	def __str__(self):
		return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):#to map the 'varchar' type
	
	def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
		super().__init__(name, ddl, primary_key, default)



class Model(dict, metaclass=ModelMetaclass):#the base class of ORM mapping

	def __init__(self, **kw):
		super(Model, self).__init__(**kw)

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

	def getValue(self, key):
		return getattr(self, key, None)

	def getValueOrDefault(self, key):
		value = getattr(self, key, None)
		if value is None:
			field = self.__mappings__[key]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				logging.debug('using default vlaue for %s: %s' % (key, str(value)))
				setattr(self, key, value)
		return value

class ModelMetaclass(type):#to read the mapping information of concrete subclass such as 'User'
	
	def __new__(cls, name, bases, attrs):
		if name = 'Model':
			return type.__new__(cls, name, bases, attrs)

