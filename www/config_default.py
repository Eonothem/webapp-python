#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Eonothem'

'''
Default configuration file
'''

configs = {
	'debug':True,
	'db': {
		'host': '127.0.0.1',
		'port': 3306,
		'user': 'www-data',
		'password': 'www-data',
		'db': 'awesome'
	},
	'session': {
		'secret': 'Awesome'
	}
}

