# Workload Analyzer

This module analyzes a workload after it is run.

(For now, it only supports OpenWhisk activations.)

## How to use Workload Analyzer

1. The **Synthetic Workload Invoker** should be run first.
2. Then run the Workload Analyzer:
```
python WorkloadAnalyzer.py -r -p
```
3. Certain features can be controlled by input arguments:
    1. `-v` or `--verbose`: prints the detailed test data
    2. `-p` or `--plot`: plots the test results
    3. `-s` or `--save_plot`: save test result plots (this option should be used with `-p`)
    4. `-a` or `--archive`: archive the test results in an pickle file (in the `data_archive` directory)
    5. `-c` or `--capacity_factor`: returns the capacity factor for functions in the workload (stored as JSON in `workload_analyzer/capacity_factors.json`)
    6. `-o` or `--override_testname`: this option is followed by the new test name. Allows assigning new names to tests, which is specifically useful for archivning with desired names.
    7. `-r` or `--read_results`: also gather the results of function invocations
4. Analysis logs can be found in `../logs/WA.log`.

## Required Packages (beyond standard libraries)

* matplotlib
* pandas
* seaborn

#### Important Note:
The `wskutil.py` script has been taken from the OpenWhisk project (https://github.com/apache/openwhisk/blob/master/tools/admin/wskutil.py) with no modifications. It holds the original Apache 2.0 license.
