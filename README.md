# [FaaSProfiler](http://parallel.princeton.edu/FaaSProfiler.html) &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/PrincetonUniversity/faas-profiler/blob/master/LICENSE)

FaaSProfiler is a tool for testing and profiling FaaS platforms. We built FaaSProfiler based on the real needs and limitations we faced early on conducting our serverless research:
* **Arbitrary mix of functions and invocation patterns**. FaaSProfiler enables the description of various invocation patterns, function mixes, and activity windows in a clean, user-friendly format.
* **FaaS-testing not plug-and-play**. Each function should be invoked independently at the right time. Precisely invoking hundreds or thousands of functions per second needs a reliable, automated tool. We achieve this with FaaSProfiler.
* **Large amount of performance and profiling data**. FaaSProfiler enables fast analysis of performance profiling data (e.g., latency, execution time, wait time, etc.) together with resource profiling data (e.g. L1-D MPKI, LLC misses, block I/O, etc.). The user can specify which parameters to profile and make use of the rich feature sets of open-source data analysis libraries like Python pandas

We have used FaaSProfiler for our research and will continue to use and improve it. We hope it accelerates testing early-stage research ideas for others by enabling quick and precise profiling of FaaS platforms on real servers. Enjoy this tool, and please don't forget citing our research paper when you use it:

Mohammad Shahrad, Jonathan Balkind, and David Wentzlaff. "[Architectural Implications of Function-as-a-Service Computing](http://parallel.princeton.edu/papers/micro19-shahrad.pdf)." 2019 52nd Annual IEEE/ACM International Symposium on Microarchitecture ([MICRO 52](https://www.microarch.org/micro52/)), October 2019.

## Setting Things Up

### Set up OpenWhisk

FaaSProfiler has been fully tested on [OpenWhisk](https://github.com/apache/openwhisk). Please make sure to set up and install [OpenWhisk](https://github.com/apache/openwhisk) before using FaaSProfiler.

**Important Note**: Some of the default [OpenWhisk configuration](https://github.com/apache/openwhisk/blob/master/ansible/group_vars/all) limits might be too restrictive for your setup. Do not forget to configure those parameters (particularly these: `invocationsPerMinute`, `concurrentInvocations`, `firesPerMinute`, and `sequenceMaxLength`).

**Note**: We plan to add support for other popular serverless platforms. Help from the community is highly appreciated.

### Configure  FaaSProfiler

After cloning this repo run the one-time configuration:
```
bash configure.sh
```

## Usage Guide

### Specify the Test 

The first step is to prepare a workload configuration file that tells FaaSProfiler about your scenario. A sample workload configuration file, called [workload_configs_local_openwhisk.json](./workload_configs_local_openwhisk.json), has been provided. You can base your own on this JSON file and configure it. Here are some details:

1. Primary fields:
    1. `test_duration_in_seconds`: Determines the length of the test in seconds.
    2. `random_seed`: If set to `null`, the randomization seed varies with time. For **deterministic** invocations set this variable to a 32-bit unsigned integer.
    3. `blocking_cli`: This true/false option determines whether consecutive invocations use blocking cli calls.
    4. `endpoint`: Specifies the endpoint type for functions to be invoked. By default, the value is set to **`"local_openwhisk"`**, which denotes functions are deployed on an OpenWhisk deployed locally (on the same machine that hosts FaaSProfiler). Changing the value to **`"generic"`** allows invoking remote functions (e.g., on AWS Lambda, Google Cloud Functions, etc.). Skimming through the [workload_configs_generic_endpoint.json](./workload_configs_generic_endpoint.json) can guide you on how to use this option. **Note that when invoking remote functions with the generic endpoint, you won't be able to do performance profiling and effectively, FaaSProfiler becomes a tool to assist you in creating precise and reproducible invocations.**
    5. `instances`: This is a collection of invocation instances. Each instance describes the invocation behavior for an application (OpenWhisk action). However, multiple instances of the same application can also be deployed with different distributions, input parameters, or activity windows to create more complicated patterns.
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
    1. `runtime_script`: This is a script that is run at the beginning of the test. Therefore, it allows specifying performance monitoring tools such as perf, pqos, or blktrace to run at the same time as the test. An example for this script is provided at [monitoring/RuntimeMonitoring.sh](./monitoring/RuntimeMonitoring.sh). This field can be ignored by setting it to `null`.
    2. `post_script`: This is a script that runs after the test ends which aims to allow automating post-analysis. This field can be ignored by setting it to `null`.

We advise the user to go over the [workload_configs.json](./workload_configs.json) file to familiarize themselves with these fields.

### Run the Test 

Simply run the following script (replace `CONFIG_FILE` with the name of your workload config file):
```
./WorkloadInvoker -c CONFIG_FILE
```
Test logs can be found in `logs/SWI.log`.

### Analyze the Test

The [Workload Analyzer](workload_analyzer) module analyzes a workload after it is run. Here is how to use it:

1. Run the Workload Analyzer:
```
./WorkloadAnalyzer -r -p
```
2. Certain features can be controlled by input arguments:
    1. `-v` or `--verbose`: prints the detailed test data
    2. `-p` or `--plot`: plots the test results
    3. `-s` or `--save_plot`: save test result plots (this option should be used with `-p`)
    4. `-a` or `--archive`: archive the test results in an pickle file (in the `data_archive` directory)
    5. `-r` or `--read_results`: also gather the results of function invocations
3. Analysis logs can be found in `logs/WA.log`.

### Compare Archived Tests

The [Comparative Analyzer](./comparative_analyzer) module compares the results of tests archived in the `data_archive` directory.

## Latest Tested Environments 

Environment/Tool | Tested Version(s)
---------------- | --------------
Python | Python 3.x
OS | Ubuntu 16.04.4 LTS, Ubuntu 20.04.1 LTS

Python Library | Latest Tested Version
---------------- | --------------
requests-futures | 1.0.0
matplotlib | 3.3.3
numpy | 1.19.5
pandas | 1.2.0
seaborn | 0.11.1
