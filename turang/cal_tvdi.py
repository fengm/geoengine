'''
File: cal_tvdi.py
Author: Min Feng
Version: 0.1
Create: 2014-08-10 21:42:46
Description: calculate TVDI from MODIS automaticly downloaded
'''

import logging

def load_area():
	from osgeo import ogr
	import config
	import geo_base_c as gb

	_shp = ogr.Open(config.cfg.get('conf', 'region'))
	_lyr = _shp.GetLayer()

	_reg = None
	for _f in _lyr:
		if _reg == None:
			_reg = gb.geo_polygon(_f.geometry().Clone())
		else:
			_reg = _reg.union(gb.geo_polygon(_f.geometry().Clone()))

	return _reg

def process_file(date, f_out, d_tmp):
	import re
	import os
	import config

	map(lambda x: os.path.exists(x) or os.makedirs(x), [os.path.dirname(f_out)])

	_tils = re.split('\s+', config.cfg.get('conf', 'tiles'))
	print 'tiles', _tils

	import mod_tvdi
	import modis_url
	import file_unzip
	with file_unzip.file_unzip(d_tmp) as _zip:
		print 'searching data'
		_ts1, _ts2 = modis_url.search_data(date)
		_fs = []

		for _tile in _tils:
			print 'process tile', _tile
			print '  > downloading data'
			_f_temp = modis_url.download_date(_ts1[_tile], _zip)
			_f_ndvi = modis_url.download_date(_ts2[_tile], _zip)

			print '  > calculate TVDI'
			_f_tvdi = _zip.generate_file('', '.tif')
			mod_tvdi.tvdi(_f_temp, _f_ndvi, _f_tvdi, _zip)
			_fs.append(_f_tvdi)

		print 'generate output file'
		_reg = load_area()
		_ext = _reg.extent()
		_div = config.cfg.getfloat('conf', 'cellsize')

		_geo = [_ext.minx, _div, 0, _ext.maxy, 0, -1 * _div]

		import math
		_rows = int(math.ceil(_ext.height() / _div))
		_cols = int(math.ceil(_ext.width() / _div))

		import geo_raster_c as ge
		import geo_raster_ex_c as gx

		_bnd_temp = ge.geo_band_info(_geo, _cols, _rows, _reg.proj, 0)

		_f_img = _zip.generate_file('', '.img')
		_f_shp = _zip.generate_file('', '.shp')

		import rasterize_band
		rasterize_band.rasterize_band(_bnd_temp, _reg, _f_img, _f_shp)

		_bnd_area = ge.open(_f_img).get_band().cache()
		_bbb = gx.geo_band_stack_zip.from_list(_fs).read_block(_bnd_temp)

		_bbb.data[_bnd_area.data == 0] = _bbb.nodata
		_f_clr = config.cfg.get('conf', 'tdvi_color')
		_bbb.save(f_out, color_table=ge.load_colortable(_f_clr), opts=['compress=lzw'])

def main():
	_opts = _init_env()

	_d_out = _opts.output

	import datetime
	_date_s = datetime.datetime.strptime(_opts.date, '%Y%m%d')
	_date_e = datetime.datetime.strptime(_opts.date, '%Y%m%d')

	import os

	_date = _date_s
	while _date <= _date_e:
		_d = _date.strftime('%Y%m%d')

		logging.info('process date %s' % _d)
		print 'date:', _d

		process_file(_d, os.path.join(_d_out, 'tvdi_%s.tif' % _d), _opts.temp)
		_date += datetime.timedelta(16)

def _usage():
	import argparse

	_p = argparse.ArgumentParser()
	_p.add_argument('--logging', dest='logging')
	_p.add_argument('--config', dest='config')
	_p.add_argument('--temp', dest='temp')

	_p.add_argument('-d', '--date', dest='date', required=True)
	_p.add_argument('-o', '--output', dest='output', required=True)

	return _p.parse_args()

def _init_env():
	import os, sys

	_dirs = ['lib', 'libs']
	_d_ins = [os.path.join(sys.path[0], _d) for _d in _dirs if \
			os.path.exists(os.path.join(sys.path[0], _d))]
	sys.path = [sys.path[0]] + _d_ins + sys.path[1:]

	_opts = _usage()

	import logging_util
	logging_util.init(_opts.logging)

	import config
	config.load(_opts.config)

	import file_unzip as fz
	fz.clean(fz.default_dir(_opts.temp))

	return _opts

if __name__ == '__main__':
	main()

