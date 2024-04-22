
import yaml

from forecaster_sha import forecaster_file_suffix_sha_map

# change the forecaster yaml files to include the sha of the forecaster and then trigger the command to deploy the forecaster and trigger the experiment

PATH_TO_FORECASTER_FILES = ""

for cur_forecaster, file_suffix_sha_map in forecaster_file_suffix_sha_map.items():
    for file_suffix, sha in file_suffix_sha_map.items():
        # read the forecaster yaml file
        with open(f"flask-{file_suffix}.yaml", 'r') as file:
            documents = list(yaml.safe_load_all(file))
            
            # change the sha in the yaml file
            if "spec" in documents[0]:
                if "template" in documents[0]["spec"]:
                    print(documents[0])
                    documents[0]["spec"]["template"]["spec"]["containers"][0]["image"] = f"docker.io/nmunshi28/flask-forecaster@sha256:{sha}"
                    print(documents[0])
                    # write the yaml file
                    with open(f"flask-{file_suffix}.yaml", 'w') as file:
                        for data in documents:
                            yaml.safe_dump(data, file, explicit_start=True)
            
            # deploy the forecaster
            command = f"ko apply -f flask-{file_suffix}.yaml"