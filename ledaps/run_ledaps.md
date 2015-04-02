
# Run LEDAPS

The code prepares input data and runs LEDAPS for atmospheric correction of Landsat TM/ETM+ data. The code has been deployed on vct02.umd.edu. Below are instructions for running the code on the server: 
Setup environment

After open a command terminal, the following script needs to be run before calling the code: 

```
source /export/data/vct02a/fengm/init_vct.sh
```

## Command usage

The code only accepts Landsat data (*.tar.gz) downloaded from USGS. It searches and processes all the Landsat data (*.tar.gz) in a folder, and output the results to a specified output folder. Usage of the command is: 

```python
python /homes/fengm/vct_02/prog/ledaps/run_ledaps.py -i <folder of Landsat data> -o <output folder> -n [number of parallel tasks]
```

### Note

1. The usage can be printed out when calling the command with "-h" parameter.

2. The output folder will be created automatically by the code if it does not exist.

3. The code processes the Landsat data found in the input data folder with a single process by default. A number higher than 1 can be given to the "-n" parameter to allow the code to process the data with parallel processes to shorter the processing time cost. The maximum number of parallel process is 24 for the VCT02 server.

### Example

* Process the Landsat data in "/homes/fengm/vct_02/test/ledaps/alaska/dn" folder with a single process: 

```python
python /homes/fengm/vct_02/prog/ledaps/run_ledaps.py -i /homes/fengm/vct_02/test/ledaps/alaska/dn -o /homes/fengm/vct_02/test/ledaps/alaska/sr
```

* Process the Landsat data in "/homes/fengm/vct_02/test/ledaps/alaska/dn" folder with three parallel processes: 

```python
python /homes/fengm/vct_02/prog/ledaps/run_ledaps.py -i /homes/fengm/vct_02/test/ledaps/alaska/dn -o /homes/fengm/vct_02/test/ledaps/alaska/sr -n 3
```

