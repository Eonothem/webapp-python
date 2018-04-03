#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Eonothem'

'''
Define URL manipulation functions

connect the ORM frame and the web frame to write the MVC
'''

import re
from coroweb import get, post
import asyncio
from models import User, Comment, Blog, next_id

@get('/')
@asyncio.coroutine
def index(request):
    users = yield from User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }

