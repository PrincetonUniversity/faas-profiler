import json
import copy

DATA_FOLDER = "../data/"
OUTPUT_FOLDER = "../output/int_config_files/"
BASE_CONFIG_FILE = "base_config.json"

RPS_LIST = [20, 40, 60, 80, 100]

ACTIVITY_WINDOW = [0, 121]

FORECASTER = "MarkovChain"

# get available pods in a map
forecaster_pod_urls = ['http://10.233.26.231',
                        'http://10.233.31.174',
                        'http://10.233.55.248',
                        'http://10.233.57.38',
                        'http://10.233.23.57',
                        ]


urls_comb = []

for i in range(len(forecaster_pod_urls)):
    urls_local = []
    for j in range(i+1):
        urls_local.append(forecaster_pod_urls[j])
    urls_comb.append(urls_local)

# for the base_config.json file use the above map to configure the json to create 1 rps applications for custom times
with open(DATA_FOLDER + BASE_CONFIG_FILE) as f:
    base_json = json.load(f)

    duplicate_base_json = copy.deepcopy(base_json)

    # print(duplicate_base_json["instances"])

    for url_comb in urls_comb: # [f1, f2]
        for rps in RPS_LIST: # 10
            base, remainder = divmod(rps, len(url_comb))
            rps_split_breakdown = [base] * len(url_comb)
            for i in range(remainder):
                rps_split_breakdown[i] += 1
            
            instance_count = 0
            for cur_url_comb, rps_split in zip(url_comb, rps_split_breakdown): # f1, 5
                for cur_app in range(rps_split):
                    url = f"{cur_url_comb}:5000/forecast/app{cur_app}"
                    
                    base_json["instances"][f"instance{instance_count}"] = {
                        "application": f"scalability{instance_count}",
                        "url": url,
                        "host": cur_url_comb,
                        "data": {
                            "conc_trace": [0.08555175341293883, 0.07690850877086178, 0.0007592824822326737, 0.0006735080458618929, 0.0006036572163231841, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.04312388480893382, 0.1363110451154214, 0.16328476508809342, 0.5, 0.9, 0.5, 0.9, 0.8],
                            "forecast_window": 1
                        },
                        "distribution": "Uniform",
                        "rate": 1,
                        "activity_window": ACTIVITY_WINDOW
                    }
                    instance_count += 1
            print(f"scalability_config_f={FORECASTER}_pc={len(url_comb)}_rps={rps}.json")
            with open(OUTPUT_FOLDER + f"scalability_config_f={FORECASTER}_pc={len(url_comb)}_rps={rps}.json", "w") as outfile:
                json.dump(base_json, outfile, indent=4)
                base_json = copy.deepcopy(duplicate_base_json)


