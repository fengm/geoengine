'''
File: modis_url.py
Author: Min Feng
Version: 0.1
Create: 2014-08-10 21:39:54
Description: generate MODIS url for downloading
'''

import numpy as np
import logging
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)

def search_url(url):
	import urllib2

	logging.info('loading ' + url)

	_url = None
	# try 5 times
	_try = 0
	while _try < 5:
		_try += 1
		try:
			_url = urllib2.urlopen(url)
			break
		except Exception:
			print '   * failed (%s)' % _try

	if _url == None:
		raise Exception('failed to load the data')

	_ts = {}
	import re
	for _l in _url.readlines():
		_m = re.search('<a href=\"(.+)\">(.+)</a>', _l)
		if _m:
			_href = _m.group(1)
			_text = _m.group(2)

			_link = url + ('' if url.endswith('/') else '/') + _href
			_ma = re.search('(h\d{2}v\d{2}).+\.hdf$', _text)
			if _ma:
				_ts[_ma.group(1)] = _link

	return _ts

def search_data(date):
	import datetime

	_date1 = datetime.datetime.strptime(date, '%Y%m%d')
	_jday = ((int(_date1.strftime('%j')) - 1) / 16) * 16 + 1
	_date2 = datetime.datetime.strptime('%04d-%03d' % (_date1.year, _jday), '%Y-%j')

	import config
	if config.cfg.getboolean('conf', 'daily'):
		_url = 'http://e4ftl01.cr.usgs.gov/MOLT/MOD11A1.005/%s/' % _date1.strftime('%Y.%m.%d')
	else:
		_url = 'http://e4ftl01.cr.usgs.gov/MOLT/MOD11A2.005/%s/' % _date2.strftime('%Y.%m.%d')
	_ts1 = search_url(_url)

	_url = 'http://e4ftl01.cr.usgs.gov/MOLT/MOD13A2.005/%s/' % _date2.strftime('%Y.%m.%d')
	_ts2 = search_url(_url)

	return _ts1, _ts2

def download_date(url, fzip):
	import config
	import os

	_d_cache = config.cfg.get('conf', 'cache')
	if _d_cache:
		_f_out = os.path.join(_d_cache, url.split('/')[-1])
		if os.path.exists(_f_out):
			return _f_out
		os.path.exists(_d_cache) or os.makedirs(_d_cache)
	else:
		_f_out = fzip.generate_file('', url.split('/')[-1])

	import urllib2
	_url = urllib2.urlopen(url)

	with open(_f_out, 'wb') as _fo:
		_block = 1024
		while True:
			_buf = _url.read(_block)
			if not _buf:
				break

			_fo.write(_buf)

	return _f_out
