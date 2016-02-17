# Data Layers for Zambia
___Min Feng, 02/16/2016___

## 30 m resolution classification maps

* __zambia_reg_sin_30m.zip__: 30m resolution map for Zambia.

### Values in the layer:

Value | Description
---: | :---
0 | nodata
1 |  maize
2 | other crops
10 | non crop

* __zambia_reg_sin_30m_err.zip__: 30 m resolution probability map for Zambia.

## 500 m resolution aggregated percentage maps

Value range of the layers are between 0 to 100, representing 0% to 100%.

* __zambia_reg_sin_500m_maize.zip__: aggregated percent of maize at 500m resolution for Zambia

* __zambia_reg_sin_500m_other_crops.zip__: aggregated percent of other crops at 500m resolution for Zambia

* __zambia_reg_sin_500m_non_crop.zip__: aggregated percent of non-crop at 500m resolution for Zambia

## File Format

GeoTIFF format with BYTE value type.

## Coordinate Reference System

Item | Parameter
---:|---
Projection        | Sinusoidal Equal Area Projection
Earth radius      | 6371007.181000 meters
Projection origin | 0° latitude, 0° longitude
Orientation       | 0° longitude, oriented vertically at top

