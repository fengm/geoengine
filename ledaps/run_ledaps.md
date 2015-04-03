
# Run LEDAPS

The code prepares input data and runs LEDAPS for atmospheric correction of Landsat TM/ETM+ data. The code has been deployed on __vct02.umd.edu__. Below are instructions for running the code on the server: 
Setup environment

After open a command terminal, the following script needs to be run before calling the code: 

```csh
source /export/data/vct02a/fengm/init_vct.sh
```

## Command usage

The code only accepts Landsat data (*.tar.gz) downloaded from USGS. It searches and processes all the Landsat data (*.tar.gz) in a folder, and output the results to a specified output folder. Usage of the command is: 

```csh
python /homes/fengm/vct_02/prog/ledaps/run_ledaps.py -i <folder of Landsat data> -o <output folder> -n [number of parallel tasks]
```

### Note

1. The usage can be printed out when calling the command with "-h" parameter.

2. The output folder will be created automatically by the code if it does not exist.

3. The code processes the Landsat data found in the input data folder with a single process by default. A number higher than __1__ can be given to the "__-n__" parameter to allow the code to process the data with parallel processes to shorter the processing time cost. The maximum number of parallel process is __24__ for the VCT02 server.

### Example

* Process the Landsat data in _/homes/fengm/vct_02/test/ledaps/alaska/dn_ folder with a single process: 

```csh
python /homes/fengm/vct_02/prog/ledaps/run_ledaps.py -i /homes/fengm/vct_02/test/ledaps/alaska/dn -o /homes/fengm/vct_02/test/ledaps/alaska/sr
```

* Process the Landsat data in _/homes/fengm/vct_02/test/ledaps/alaska/dn_ folder with three parallel processes: 

```csh
python /homes/fengm/vct_02/prog/ledaps/run_ledaps.py -i /homes/fengm/vct_02/test/ledaps/alaska/dn -o /homes/fengm/vct_02/test/ledaps/alaska/sr -n 3
```

