'''
File: mod_tvdi.pyx
Author: Min Feng
Version: 0.1
Create: 2014-08-10 21:35:35
Description: calculate the TVDI using MODIS data
'''
import numpy as np
import logging
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)

def mad(data, axis=None):
	import numpy as np
	return np.mean(np.absolute(data - np.mean(data, axis)), axis)

def tvdi(f_lst, f_ndvi, f_out, fzip):
	import geo_raster_c as ge
	import numpy as np

	# _bnd_lst = ge.open(fzip.unzip(f_lst)).get_band().cache()
	# _bnd_ndvi = ge.open(fzip.unzip(f_ndvi)).get_band().cache()

	_bnd_lst = ge.open(fzip.unzip(f_lst)).get_subdataset('LST_Day_1km').get_band().cache()
	_bnd_ndvi = ge.open(fzip.unzip(f_ndvi)).get_subdataset('NDVI').get_band().cache()

	_dat_lst = _bnd_lst.data
	_dat_ts = _dat_lst * 0.02
	_ta = _dat_ts[(_dat_ts > 260) & (_dat_ts < 320)].min() + 2

	_dat_ndvi = _bnd_ndvi.data.astype(np.float32) / 10000.0

	_mm = 20
	_nn = 100

	_ts_max = np.empty(_mm, dtype=np.float32)
	_ndvi_ts = np.empty(_mm, dtype=np.float32)
	_temp = np.empty(_nn, dtype=np.float32)

	_ts_max.fill(-1)
	_ndvi_ts.fill(-1)

	for i in xrange(_mm):
		_temp.fill(-1)

		for j in xrange(_nn):
			_ps = _dat_ts[(((i*1.0/_mm+j*1.0/_mm/_nn) <= _dat_ndvi) & \
					(_dat_ndvi < (i*1.0/_mm+(j+1)*1.0/_mm/_nn)) & \
					(_dat_ts >= 200) & (_dat_ts <= 350) & \
					(0 < _dat_ndvi) & (_dat_ndvi < 1))]
			if _ps.size > 0:
				_temp[j] = _ps.max()

		_num = 0
		_temp_sel = _temp[_temp > 0]

		if _temp_sel.size > 5:
			while _temp_sel.size > 5 and _num < 10:
				_sigma = mad(_temp_sel)
				_avg = _temp_sel.mean()

				_temp_t = _temp_sel[_temp_sel-_avg > -0.5 * _sigma]
				if _temp_t.size > 0:
					_temp_sel = _temp_t

				_num += 1

			_ts_max[i] = _temp_sel.mean()

		_ndvi_ts[i] = i * 1.0/_mm

	from scipy import stats
	_se = 99.0
	_res4 = [0, 0]
	_deter_coeff = 0

	_idx = _ts_max > 0
	_num = _ts_max[_idx].size

	if _num > 0:
		_line = stats.linregress(_ndvi_ts[_idx], _ts_max[_idx])
		_res4 = [_line[1], _line[0]]
		_ts_mean = _ts_max[_idx].mean()
		_count = 0
		while _se > 0.5 and _count < 5:
			_sum1 = 0
			_sum4 = 0
			for j in xrange(_idx.size):
				if _idx[j] == False:
					continue

				_sum1 += (_ts_max[j] - (_res4[0] + _res4[1] * _ndvi_ts[j])) ** 2
				_sum4 += (_ts_max[j] - _ts_mean) ** 2

			_se = ((_sum1 / (_num - 2)) ** 0.5) if _num > 2 else 0
			_deter_coeff = 1 - _sum1 / _sum4

			_count += 1

	logging.info('params: %s, %s, %s, %s' % (_res4[0], _res4[1], _deter_coeff, _se))
	# print (_res4[0], _res4[1], _deter_coeff, _se)

	_rows = _bnd_ndvi.height
	_cols = _bnd_ndvi.width

	_dat_tvdi = np.empty((_rows, _cols), dtype=np.float32)
	_dat_tvdi.fill(0)

	for _row in xrange(_rows):
		for _col in xrange(_cols):
			_tmax = _res4[0] + _res4[1] * _dat_ndvi[_row, _col]
			_tmin = _ta

			_dat_tvdi[_row, _col] = (_dat_ts[_row, _col] - _tmin) / (_tmax - _tmin)

	_dat_tvdi[_dat_tvdi > 1] = 1
	_dat_tvdi[(_dat_tvdi < 0) | ((-1 <= _dat_ndvi) & (_dat_ndvi < 0))] = 0

	_bnd_tdvi = _bnd_ndvi.from_grid((_dat_tvdi * 100).astype(np.uint8))
	_bnd_tdvi.nodata = 255
	_bnd_tdvi.save(f_out)

