# Data Layers for Zambia
___Min Feng, 02/16/2016___

## 30 m resolution classification maps

  __Image size__: 44503 x 36528
  
  __Layers__:

  * __zambia_reg_sin_30m.zip__: 30m resolution map for Zambia.

    __Value type__: BYTE
    __Values in the layer__:
    
    Value | Description
    ---: | :---
    0 | nodata
    1 |  maize
    2 | other crops
    10 | non crop

  * __zambia_reg_sin_30m_err.zip__: 30 m resolution probability map for Zambia.

    __Value range__:  0.0 ~ 1.0
    
    __Nodata__: -9999
    
    __Value type__: float32
  
## 500 m resolution aggregated percentage maps

  __Value range__: between 0 to 100, representing 0% to 100%.
  
  __Value type__: BYTE
  
  __Image size__: 2670 x 2191
  
  __Layers__:

    * __zambia_reg_sin_500m_maize.zip__: aggregated percent of maize at 500m resolution for Zambia
    
    * __zambia_reg_sin_500m_other_crops.zip__: aggregated percent of other crops at 500m resolution for Zambia
    
    * __zambia_reg_sin_500m_non_crop.zip__: aggregated percent of non-crop at 500m resolution for Zambia

## File Format

  GeoTIFF format

## Coordinate Reference System

  Item | Parameter
  ---:| :---
  Projection        | Sinusoidal Equal Area Projection
  Earth radius      | 6371007.181000 meters
  Projection origin | 0° latitude, 0° longitude
  Orientation       | 0° longitude, oriented vertically at top

