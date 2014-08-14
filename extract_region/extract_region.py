
def load_region(f_shp, cel):
	from osgeo import ogr

	_shp = ogr.Open(f_shp)
	_lyr = _shp.GetLayer()

	_ext = _lyr.GetExtent()
	_prj = _lyr.GetSpatialRef()

	import geo_base_c as gb
	_eee = gb.geo_extent(_ext[0], _ext[2], _ext[1], _ext[3], _prj)

	import math
	_row = int(math.ceil(_eee.height() / cel))
	_col = int(math.ceil(_eee.width() / cel))

	_geo = [_eee.minx, cel, 0, _eee.maxy, 0, -1 * cel]

	import geo_raster_c as ge
	return ge.geo_band_info(_geo, _col, _row, _prj)

def main():
	_opts = _init_env()

	_bnd_tmp = load_region(_opts.region, _opts.cell)

	import os
	_check_ext = lambda x: os.path.splitext(x)[-1].lower() in ['.img', '.tif']

	_fs = []
	for _root, _dirs, _files in os.walk(_opts.input):
		for _file in _files:
			if not _check_ext(_file):
				continue

			_fs.append(os.path.join(_root, _file))

	_d_out = _opts.output
	os.path.exists(_d_out) or os.makedirs(_d_out)

	import geo_raster_c as ge
	import progress_percentage
	import file_unzip

	with file_unzip.file_unzip(_opts.temp) as _zip:
		_ppp = progress_percentage.progress_percentage(len(_fs))

		for _f in _fs:
			_ppp.next(count=True, message=os.path.basename(_f))

			_f_out = os.path.join(_d_out, os.path.basename(_f))
			_bnd = ge.open(_zip.unzip(_f)).get_band().read_block(_bnd_tmp)
			_bnd.save(_f_out)

		_ppp.done()

def _usage():
	import argparse

	_p = argparse.ArgumentParser()
	_p.add_argument('--logging', dest='logging')
	_p.add_argument('--config', dest='config')
	_p.add_argument('--temp', dest='temp')

	_p.add_argument('-i', '--input', dest='input', required=True)
	_p.add_argument('-r', '--region', dest='region', required=True)
	_p.add_argument('-c', '--cell', dest='cell', required=True, type=float)
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

