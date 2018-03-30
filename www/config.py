#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Eonothem'

'''
Configuration
'''

import config_default

class Dict(dict):
	'''
	Simple dict but support access as x.y style.
	'''
	def __init__(self, names=(), values=(), **kw):
		super(Dict, self).__init__(**kw)
		for k, v in zip(names, values):
			self[k] = v

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

def merge(defaults, override):
	'''
	cover configuration file, and update default configuration
	'''
	r = {}
	for name, value in defaults.items():
		if name in override:
			if isinstance(value, dict):
				r[name] = merge(value, override[name])
			else:
				r[name] = override[name]
		else:
			r[name] = defaults[name]
	return r 

def toDict(d):
	D = Dict()
	for k, v in d.items():
		D[k] = toDict(v) if isinstance(v, dict) else v
	return D

configs = config_default.configs

try:
	import config_override
	merge(configs, config_override.configs)
except ImportError:
	pass

configs = toDict(configs)

