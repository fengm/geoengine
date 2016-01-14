
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

# path to the temporary folder. The code will use the tmp folder by default
temp=

# the WRS2 tile for processing. The code uses the tile of the first SR input file by default.
tile=

# switch for running the udist, udistComposite, changeAnalysis modules (1: on, 0: off)
udist=1
udistComposite=1
changeAnalysis=1

# maximum number of Landsat scenes for each year
max_scenes_per_year=3

[path]

# path to the DEM data
dem=/export/data/bessie1/fengm/data/dem/ext/gls_dem_tif.shp

# path to the land cover data
landcover=/export/data/bessie2/zhao26/feng_out/sr_to_cheng_11242015/p048r022/CANADA_NLCD_p048r022

# path to the udist, udistComposite, changeAnalysis modules
bin=%(root)s/bin
```

# Command usage

The code only accepts Landsat SR produced by LEDAPS. It searches and processes all the LEDAPS processed Landsat SR (*.hdf) in a folder, and output the results to a specified output folder. Usage of the command is:

```csh
usage: vct.py -i INPUT -o OUTPUT
              [--tile TILE]
              [--udist 1/0]
              [--udistComposite 1/0]
              [--changeAnalysis 1/0]
```
- `-h`, print out the usage.
- `-i INPUT`, folder of Landsat SR or list of Landsat SR files.
- `-o OUTPUT`, path of the output folder.
- `--tile`, the WRS2 tile for processing. The code uses the tile of the first SR input file by default.
- `--udist`, enable/disable the udist module (default: 1).
- `--udistComposite`, enable/disable the udistComposite module (default: 1).
- `--changeAnalysis`, enable/disable the changeAnalysis module (default: 1).

Note
- The input SR format can be either HDF or ENVI
- The output folder will be created automatically by the code if it does not exist.

# Example

```csh
/export/data/vct02a/fengm/prog/vct/vct.py -i /data/vct02a/mli12310/1228/ledaps/composites -o /export/data/vct02a/fengm/prog/vct/test
```

Note: the test run results of the above example command can be found at the specified output folder:

```csh
/export/data/vct02a/fengm/prog/vct/test
```

# Update

## 01/13/2016
1. support both HDF and ENVI format as input SR data format.
2. input SR can be either a folder or a text file (.txt) that provides the list of SR files. 
3. pick scenes from the input SR files for each year to provide maximum clear observations with minimum Landsat scenes.
4. allow enable/disable udist, udistComposite, changeAnalysis modules
5. minor bugs fixed

