#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Eonothem'

'''
Define URL manipulation functions
'''

import asyncio
from coroweb import get, post
from models import User, Comment, Blog, next_id
import re, time, json, logging, hashlib, base64
from aiohttp import web
from apis import APIError, APIValueError, APIResourceNotFoundError
from config import configs

COOKIE_NAME = 'swesession'
_COOKIE_KEY = configs.session.secret

def user2cookie(user, max_age):
	'''
	Generate cookie str by user.
	'''
	expires = str(int(time.time() + max_age))
	s= '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
	L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
	return '-'.join(L)

@get('/register')
@asyncio.coroutine
def register():# show the register page
	return {
		'__template__': 'register.html'
	}

@get('/signin')
def signin():
	return {
		'__template__': 'signin.html'
	}

'''
@get('/')
@asyncio.coroutine
def handler_url_blog(request):
	body = '<h1>Awesome</h1>'
	return body
'''
@get('/')
@asyncio.coroutine
def index(request):
	summary = 'Hello, World.'
	blogs = [
    	Blog(id='1', name='Test Blog', summary=summary, create_at=time.time()-120),
    	Blog(id='2', name='Something New', summary=summary, create_at=time.time()-3600),
    	Blog(id='3', name='Learn Swift', summary=summary, create_at=time.time()-7200)
    ]
	return {
        '__template__': 'blogs.html',
        'blogs': blogs,
        '__user__': request.__user__
    }

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@post('/api/users')
@asyncio.coroutine
def api_register_user(*, email, name, passwd):
	if not name or not name.strip():
		raise APIValueError('name')
	if not email or not _RE_EMAIL.match(email):
		raise APIValueError('email')
	if not passwd or not _RE_SHA1.match(passwd):
		raise APIValueError('passwd')
	users = yield from User.findAll('email=?', [email])
	if len(users) > 0:
		raise APIError('register:failed', 'email', 'Email is already in use.')
	uid = next_id()
	sha1_passwd = '%s:%s' % (uid, passwd)
	user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
	yield from user.save()

	#make session cookie:
	r = web.Response()
	r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
	user.passwd = '******'
	r.content_type = 'application/json'
	r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
	return r

