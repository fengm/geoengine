
The code prepares input data and runs VCT to detect forest cover change. The code has been deployed on __vct02.umd.edu__. Below are instructions for running the code on the server:

# Setup environment:

After open a command terminal, the following script needs to be run before calling the VCT code:

```csh
source /export/data/vct02a/fengm/init_vct.sh
```

# Command usage:

The code only accepts Landsat SR produced by LEDAPS. It searches and processes all the LEDAPS processed Landsat SR (*.hdf) in a folder, and output the results to a specified output folder. Usage of the command is:

```csh
python /export/data/vct02a/fengm/prog/vct/vct.py -i [folder of Landsat SR] -o [output folder]
```

Note:

1. The usage can be printed out when calling the command with "__-h__" parameter.

2. The output folder will be created automatically by the code if it does not exist.

# Example:

```csh
python /export/data/vct02a/fengm/prog/vct/vct.py -i /data/vct02a/mli12310/1228/ledaps/composites -o /export/data/vct02a/fengm/prog/vct/test
```

Note: the test run results of the above example command can be found at the specified output folder:

```csh
/export/data/vct02a/fengm/prog/vct/test
```
