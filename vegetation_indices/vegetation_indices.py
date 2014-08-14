#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
File: calculate_index.py
Author: Min Feng
Version: 0.1
Create: 2014-05-20 11:48:05
Description: calculate NDVI, SAVI, MSAVI
'''
'''
Version: 0.2
Date: 2014-05-24 20:55:35
Note: add LAI algorithm and support Landsat SR in tar.gz format
'''

import logging

def qa_mask(bnd):
	pass

def alg_lai(bnd_savi):
	import numpy as np

	_dat = bnd_savi.data_ma.astype(np.float32) / 1000.0
	_dat = 0.69 - _dat
	_dat[_dat <= 0] = 0.00001

	_ddd = (np.log(_dat / 0.59)) / 0.91
	_ddd = _ddd * 1000.0

	return bnd_savi.from_ma_grid(_ddd.astype(np.int16))

def calclate_index(bnd1, bnd2, l):
	import numpy as np
	_dat1 = bnd1.data_ma.astype(np.float32) / 10000.0
	_dat2 = bnd2.data_ma.astype(np.float32) / 10000.0

	_dat1[_dat1 <= 0] = 0.00000001
	_dat2[_dat2 <= 0] = 0.00000001

	_dat1[_dat1 > 1] = 1
	_dat2[_dat2 > 1] = 1

	_cs = {
			'ndvi': lambda d1, d2, l: (d1 - d2) / (d1 + d2),
			'savi': lambda d1, d2, l: (d1 - d2) * (1 + l) / (d1 + d2 + l),
			'msavi': lambda d1, d2, l: ((2.0 * d1) + 1 - (((2.0 * d1 + 1.0) ** 2 - 8.0 * (d1 - d2)) ** 0.5)) / 2
			}

	_bs = {}
	for _n, _c in _cs.items():
		print 'calculate', _n
		_dat = _c(_dat1, _dat2, l)
		_dat = _dat * 1000.0
		_bs[_n] = bnd1.from_ma_grid(_dat.astype(np.int16))

	_bs['lai'] = alg_lai(_bs['savi'])

	return _bs

def load_bands_from_image(f_img, bnds):
	import geo_raster_c as ge

	_img = ge.open(f_img)

	_ls = {}
	for _n, _b in bnds.items():
		print 'loading band', _n.upper()
		logging.info('loading band %s: %s' % (_n, _b))
		_ls[_n] = _img.get_band(_b).cache()

	return _ls

def load_bands(f_img, dt, fzip):
	import geo_raster_c as ge

	_ls = {}

	if dt.startswith('landsat'):
		_bs = {'nir': 5, 'red': 4} if dt == 'landsat8' else {'nir': 4, 'red': 3}

		import os
		_f = f_img

		if _f.endswith('.tar.gz'):
			_fs = extract_landsat_gz(_f, fzip.generate_file('', ''))
			if 'sr' not in _fs.keys():
				raise Exception('failed to find SR file in the package')

			_f = _fs['sr']

			logging.info('loading sr file %s' % _f)
			if not _f.endswith('.hdf'):
				raise Exception('Only support Landsat SR in HDF format (%s)' % _f)

			_img = ge.open(_f)

			for _n, _b in _bs.items():
				print 'loading band', _n.upper()
				logging.info('loading band %s: %s' % (_n, _b))
				_ls[_n] = _img.get_subdataset(_b).get_band().cache()

		elif os.path.splitext(fzip.unzip(_f))[1].lower() in ['.img', '.tif']:
			_ls = load_bands_from_image(_f, _bs)
		else:
			raise Exception('unsupported data format %s' % _f)

	if dt == 'modis':
		if not f_img.endswith('.zip'):
			raise Exception('Only support MODIS SR in zip package')

		_bs = {'nir': 2, 'red': 1}
		_fs = extract_modis_zip(f_img, fzip.generate_file('', ''))

		for _n, _b in _bs.items():
			print 'loading band', _n
			logging.info('loading band %s: %s' % (_n, _b))
			_ls[_n] = ge.open(_fs[_b]).get_band().cache()

	_ss = None
	for _b in _ls.values():
		_b.nodata = _b.get_nodata()
		if _ss == None:
			_ss = (_b.width, _b.height)
		else:
			if _b.width != _ss[0] or _b.height != _ss[1]:
				raise Exception('the band size do not match')

	return _ls

def process_scene(f_img, dt, s_factor, f_out, fzip):
	import os

	_bs = load_bands(f_img, dt, fzip)
	_rs = calclate_index(_bs['nir'], _bs['red'], s_factor)

	(lambda x: os.path.exists(x) or os.makedirs(x))(os.path.dirname(f_out))

	for _n, _b in _rs.items():
		print 'write', _n
		logging.info('write band %s' % _n)
		_b.save(f_out % _n, opts=['compress=lzw'])

def tree():
	import collections
	return collections.defaultdict(tree)

def extract_landsat_gz(f_zip, d_out):
	import re
	import os

	os.path.exists(d_out) or os.makedirs(d_out)

	_fs = {}
	import tarfile
	with tarfile.open(f_zip, 'r:gz') as _zip:
		for _f in _zip:
			_m = re.match('^lndsr\..+\.hdf$', _f.name)
			if _m == None:
				continue

			if 'ndvi' in _f.name:
				continue

			logging.info('unzip %s to %s' % (_f.name, d_out))
			_zip.extract(_f, d_out)
			_f_out = os.path.join(d_out, _f.name)
			_fs['sr'] = _f_out

	return _fs

def extract_modis_zip(f_zip, d_out):
	import re
	import os

	os.path.exists(d_out) or os.makedirs(d_out)

	_fs = {}
	import zipfile
	with zipfile.ZipFile(f_zip, 'r') as _zip:
		for _f in _zip.filelist:
			_m = re.search('B(\d)_REFL', _f.filename)
			if _m == None:
				continue

			logging.info('unzip %s to %s' % (_f.filename, d_out))
			_f_out = os.path.join(d_out, _f.filename)
			_zip.extract(_f, d_out)
			_fs[int(_m.group(1))] = _f_out

	return _fs

def identify_scenes(d_in, dt, s_factor, d_out, fzip):
	import os

	_fs = {}
	for _root, _dirs, _files in os.walk(d_in):
		for _file in _files:
			if _file[-4:] not in ['.zip', '.hdf', 'r.gz', '.img', '.tif']:
				continue

			_fs[_file] = os.path.join(_root, _file)

	print 'found', len(_fs.keys()), 'files'

	for _n, _f in _fs.items():
		print '>', _n

		_f_out = os.path.join(d_out, '%s_%%s.tif' % (_n[:-7] if _n.endswith('.tar.gz') else _n[:-4],))
		process_scene(_f, dt, s_factor, _f_out, fzip)

def main():
	_opts = _init_env()

	print 'input:', _opts.input
	print 'data type:', _opts.data_type
	print 'output:', _opts.output

	import file_unzip
	with file_unzip.file_unzip(_opts.temp) as _zip:
		identify_scenes(_opts.input, _opts.data_type.lower(), _opts.factor, _opts.output, _zip)

def _usage():
	import argparse

	_p = argparse.ArgumentParser()
	_p.add_argument('--logging', dest='logging')
	_p.add_argument('--config', dest='config')
	_p.add_argument('--temp', dest='temp')

	_p.add_argument('-i', '--input', dest='input', required=True)
	_p.add_argument('-l', '--factor', dest='factor', required=True, type=float, help='soil brightness correction factor')
	_p.add_argument('-d', '--data-type', dest='data_type', choices=['landsat', 'landsat8', 'modis'], default='modis')
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
	try:
		main()
	except KeyboardInterrupt:
		print '\n\n* User stopped the program'
	except Exception, err:
		import traceback

		logging.error(traceback.format_exc())
		logging.error(str(err))

		print '\n\n* Error:', err

