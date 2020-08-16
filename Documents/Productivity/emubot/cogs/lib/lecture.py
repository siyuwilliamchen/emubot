"""
author: William Chen
"""

class Lecture():

	def __init__(self, name, period, userid, zoomlink = "unavailable",):
		self.name = name
		self.period = period
		self.userid = userid
		self.zoomlink = zoomlink


	def updateZoom(self, zoomlink):
		self.zoomlink = zoomlink

	def updateuserid(self, userid):
		self.techer = userid

	def toList(self):
		return [self.name, self.period, self.userid, self.zoomlink]