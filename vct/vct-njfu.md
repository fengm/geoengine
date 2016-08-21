# Landsat VCT

The code prepares input data and runs VCT to detect forest changes using time-serial Landsat images.


----------

## Step 1: Prepare Landsat SR data

VCT requires Landsat SR images, with ENVI format and band combination of:

`Blue, Green, Red, NIR, SWIR1, SWIR2, Thermal`

A seperate code was developed to convert the orginal Landsat SR to format that meets the requirement of VCT:
 
    /opt/prog/run/convert_sr.py -i <input folder> -o <output folder>

For example:

```csh
/opt/prog/run/convert_sr.py -i "/home/lms/Downloads/p123r023" -o "/media/lms/data1/mfeng/test/sr3"
```

----------

##Step 2: Setup config file

Make a copy of the config file at

    /opt/prog/run/conf/vct.conf

 
Edit the items to update the path to land cover and DEM files
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
dem=<path to DEM data set>

# path to the land cover data
landcover=<path to land cover data set>

# path to the udist, udistComposite, changeAnalysis modules, no need to change it
bin=%(root)s/bin
```

Note: the land cover data set needs to use NLCD classification scheme.

----------

## Step 3: Run VCT

    usage: vct.py -i <input SR folder> -o <output folder> --config <config file>
 
For example:

```csh
/opt/prog/run/convert_sr.py -i "/home/lms/Downloads/p123r023" -o "/media/lms/data1/mfeng/test/sr3" 
```

Note:

* Do not use "space" in file and folder paths
* The Landsat SR images need to be in UTM CRS

