# -*- coding: utf-8 -*-

class Screen(object):
	
	def __init__(self):
		self._resolution = 1200#实例化时赋值resolution

	@property
	def width(self):
		return self._width
	@width.setter
	def width(self, value):
		self._width = value

	@property
	def height(self):
		return self._height
	@height.setter
	def height(self, value):
		self._height = value

	@property
	def resolution(self):
		return self._resolution

#test:
s = Screen()
s.width = 1024
s.height = 768
print(s.resolution)
print(s.width)
print(s.height)
