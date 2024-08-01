
# Horizontal Scalability Experiment for FeMux Pods

## Description
The horizontal scalability experiment is built to test all deployed pods with the max RPS they can sustain given each pod has a fixed CPU and memory limit. This module has 3 parts:

### Traffic Files Generator:
The [scalability_json_generator.py](./scalability_experiments/code/scalability_json_generator.py) in `scalability_experiments/code` is responsible for using the `based_config.json` and populating custom `config_files` in the format 
`scalability_config_f={forecaster-name}_pc={pod-count}_rps={RPS}.json`
in the `output/` directory. These files are then used by *faas-profiler* for triggering the traffic received by the `flask-forecasters` deployed in Knative (See `alm-analysis-prediction-models/femux-online/README.md`).

After all femux-forecaster pods have been deployed you can update *forecaster_pod_urls* parameter in the [scalability_json_generator.py](./scalability_experiments/code/scalability_json_generator.py) to use the IP addresses for the forecaster pods. *ACTIVITY_WINDOW* maintains the same RPS for 2 minutes to get enough response time data.

### Request Latency Extraction Unit:
In the [scalability_experiment.py](./scalability_experiment.py) we play the above generated workload invoker config files to ensure each experiment is run and the response time for the respective RPS is captured in a Dataframe.

### Post-processing:
The post-processing module ([testing.ipynb](./scalability_experiments/code/testing.ipynb)) is then used to further visualise the response time Dataframe per forecaster per RPS. It also combines the response time data proportional to the number of blocks won per cluster. This post processing module uses the RPS information and response times across experiments and generates plots for both average and p99 latency of horizontally scaled femux pods.

## Setup
The requirements to execute the horizontal scalability experiment are:
1. `faas-profiler` setup using:
```
bash configure.sh
```
2. FeMux pods should be deployed in Knative (See `alm-analysis-prediction-models/femux-online/README.md`).


## Getting Started
1. Generate config files for desired forecaster and RPS in the `scalability_experiments/` directory:
```
python3 scalability_json_generator.py
```
The config_files are generated in `output/config_files/` (Note: only use the RPS files you desire proportional to the number of pods.)

2. Trigger the request latency extraction unit to get the response time dataframe for each forecaster and RPS:
```
python3 scalability_experiment.py
```

3. Run post-processing ([testing.ipynb](./scalability_experiments/code/testing.ipynb)) after generating all scalability data in the `output/scalability_data/` directory. This will generate the desired horizontal scalability experiment plot combining all RPS and forecaster pairs.