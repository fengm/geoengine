
The code prepares input data and runs VCT to detect forest cover change. 

It has been deployed on:

`vct02.umd.edu` at `/export/data/vct02a/fengm/prog/vct`

`bessie.umd.edu` at `/export/data/bessie1/fengm/prog/vct`

Below are instructions for running the code on the server:

# Setup environment

After open a command terminal, the following script needs to be run before calling the VCT code:

## VCT02

```csh
source /export/data/vct02a/fengm/init_vct.sh
```

## Bessie

```csh
source /export/data/bessie1/fengm/init_bessie.sh
```

# Configuration

The configuration file can be found at`conf/vct.conf`.

```ini
[conf]

# the WRS2 tile for processing. The code uses the tile of the first SR input file
#    when no tile provided
tile=

# switch for running the udist, udistComposite, changeAnalysis modules (1: on, 0: off)
udist=1
udistComposite=1
changeAnalysis=1

# maximum number of Landsat scenes for each year, 3 by default
max_scenes_per_year=3

[path]

# path to the DEM data
dem=/export/data/bessie1/fengm/data/dem/ext/gls_dem_tif.shp

# path to the land cover data
landcover=<path to the land cover data set>

# path to the udist, udistComposite, changeAnalysis modules, no need to change it
bin=%(root)s/bin
```

# Command usage

The code only accepts Landsat SR produced by LEDAPS. It searches and processes all the LEDAPS processed Landsat SR (*.hdf) in a folder, and output the results to a specified output folder. Usage of the command is:

```csh
usage: vct.py -i INPUT -o OUTPUT --config CONFIG
              [--tile TILE]
              [--udist 1/0]
              [--udistComposite 1/0]
              [--changeAnalysis 1/0]
              [--logging LOG]
              [--temp TEMP]
```
- `-h`, print out the usage.
- `-i INPUT`, folder of Landsat SR or list of Landsat SR files.
- `-o OUTPUT`, path of the output folder.
- `--config CONFIG`, path to the config file.
- `--tile`, the WRS2 tile for processing. The code uses the tile of the first SR input file by default.
- `--udist`, enable/disable the udist module (default: 1).
- `--udistComposite`, enable/disable the udistComposite module (default: 1).
- `--changeAnalysis`, enable/disable the changeAnalysis module (default: 1).
- `--logging LOG`, path to the log file, `vct.log` in the output folder by default.
- `--temp TEMP`, path to the folder holds all temperary files, `tmp` folder in the output folder by default.

Note
- The input SR format can be either HDF or ENVI
- The output folder will be created automatically by the code if it does not exist.

# Example

```csh
vct.py -i /export/data/bessie2/zhao26/feng_out/sr_to_cheng_11242015/p048r022 -o test --config conf/vct.conf'
```

# Update

## 01/16/2016
* config file is required for running the code
* change the location of log file and temp folder to the output folder by default

## 01/13/2016
* support both HDF and ENVI format as input SR data format.
* input SR can be either a folder or a text file (.txt) that provides the list of SR files. 
* pick scenes from the input SR files for each year to provide maximum clear observations with minimum Landsat scenes.
* allow enable/disable udist, udistComposite, changeAnalysis modules
* minor bugs fixed

