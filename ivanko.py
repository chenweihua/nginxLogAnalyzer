#!/usr/bin/nginx_log_analyzer_env python
# -*- coding: utf-8 -*-

import urllib, json
import os
import os.path

BASE_DIR = os.getcwd()

def range_ip_for_geolocation(files):
	ip_api_url = 'http://applicationfree.net:8080/najaktivniji/?format=json'
	response = urllib.urlopen(ip_api_url)
	data = json.loads(response.read())
	filename = str('/')+str(files)

	file_path = BASE_DIR+str(filename)
	my_file = os.path.exists(file_path)
	print my_file
	if my_file != 'False':
		try:
			os.remove(files)
		except:
			print 'ip file '+str(files)

	outfile = open(files, "w+")
	for ip_dictionary in data:
		ip_range = dict((key,value) for key, value in ip_dictionary.iteritems() if key == 'ip')
		for key, value in ip_range.iteritems():
			print >> outfile, value
	outfile.close()

range_ip_for_geolocation('ip.txt')