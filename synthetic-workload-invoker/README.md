# Synthetic Workload Invoker (SWI)

## How to use SWI

You need to first specifcy the workload configuration file (Similar to [workload_configs.json](../workload_configs.json)). This file has various fields:

1. Primary fields:
    1. `test_duration_in_seconds`: Determines the length of the test in seconds.
    2. `random_seed`: If set to `null`, the randomization seed varies with time. For **deterministic** invocations set this variable to a 32-bit unsigned integer.
    3. `blocking_cli`: This true/false option determines whether consecutive invocations use blocking cli calls. 
    4. `instances`: This is a collection of invocation instances. Each instance describes the invocation behavior for an application (OpenWhisk action). However, multiple instances of the same application can also be deployed with different distributions, input parameters, or activity windows to create more complicated patterns.
2. Each invocation instance:
    1. `application`: This should be the same as the OpenWhisk action name. (You can see the list of successfully built OpenWhisk actions using `wsk action list -i`)
    2. FaaSProfiler supports two invocation types. You need to select one, for each instance, and configure it accordingly.
        i. **Synthetic traffic**:
            1. `distribution`: SWI currently supports **Uniform** and **Poisson** distributions.
            2. `rate`: Function invocations per second. For a **Poisson** distribution, this is **lambda**. A rate of zero means no invocations.
        ii. **Trace-based traffic**:
            1. `interarrivals_list`: The list of interarrival times. This mode allows replaying real traces using FaaSProfiler.
    6. `activity_window`: If set to `null`, the application is invoked during the entire test. By setting a time window, one can limit the activity of the application to a sub-interval of the test. There is no need to provide this parameter when using trace-based traffic.
    7. `param_file`: This optional entry allows specifying an input parameter JSON file, similar to option `-P` in WSK CLI.
    8. `data_file`: This optional entry allows specifying binary input files such as images for the function.
3. Performance monitoring (`perf_monitoring`) field, where you can specify:
    1. `runtime_script`: This is a script that is run at the beginning of the test. Therefore, it allows specifying performance monitoring tools such as perf, pqos, or blktrace to run at the same time as the test. An example for this script is provided at [monitoring/RuntimeMonitoring.sh](../monitoring/RuntimeMonitoring.sh). This field can be ignored by setting it to `null`.
    2. `post_script`: This is a script that runs after the test ends which aims to allow automating post-analysis. This field can be ignored by setting it to `null`.

After setting this file, simply run the following script (replace `CONFIG_FILE` with the name of your workload config file):
```
./WorkloadInvoker -c CONFIG_FILE
```
Test logs can be found in `../logs/SWI.log`.

## Required Packages (beyond standard libraries)

* NumPy

## Tested Environments

Environment/Tool | Tested Version 
---------------- | --------------
Python | 3.6.5 & 3.6.8
OS | Ubuntu 16.04.4 LTS
