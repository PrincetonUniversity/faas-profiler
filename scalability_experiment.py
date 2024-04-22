
import os
import time
import subprocess
import pandas as pd

FOLDER_TYPE = 'config_files' # 'dummy_config_files' or 'config_files'

# get all files in output folder in sorted order
files = os.listdir(f'scalability_experiments/output/{FOLDER_TYPE}')

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# sort files by name
files.sort()
files.sort(key=lambda f: int(f.split('rps=')[-1].split('.')[0]))
files.sort(key=lambda f: int(f.split('pc=')[-1].split('_')[0]))

df = pd.DataFrame()

for file in files:

    # for each file, read the json and get the response time for each request
    response_times = []
    
    # get pod count from the file name
    pod_count = int(file.split('pc=')[-1].split('_')[0])
    
    # get rps from the file name
    rps = int(file.split('rps=')[-1].split('.')[0])

    # get forecaster name from the file name
    forecaster = file.split('f=')[-1].split('_')[0]

    # deploy this json file to the terminal using the command ./WorkloadInvoker -c ../output/{file}
    command = f"./WorkloadInvoker -c scalability_experiments/output/{FOLDER_TYPE}/{file}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    output = stdout.decode('utf-8', 'ignore')
    print(output)
    # get the response times from the stdout
    # the response times are in the format "response_time: <seconds>"
    response_times.append([float(line.split(': ')[1].replace('\x00', '')) for line in output.split('\n') if 'response_time:' in line and is_float(line.split(': ')[1].replace('\x00', ''))])
    df = pd.concat(
        [df, pd.DataFrame({'FORECASTER': forecaster,
                           'POD_COUNT': pod_count,
                           'RPS': rps,
                           'RESPONSE_TIMES': response_times})], ignore_index=True
    )

    df.to_pickle("scalability_experiments/output/scalability_data/mc_horizontal_scalability_data.pickle")
    time.sleep(60)
    print("completed experiment for file: ", file)
