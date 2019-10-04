# JSON 

Processing JSON inputs in common in FaaS workloads. These benchmarks process a relatively large JSON input. The benchmarks are originally adopted from this repo: https://github.com/kostya/benchmarks/tree/master/json . However, they were modified to be used by the OpenWhisk platform and use JSON parameter inside of file.

In this directory, functions are provided in *NodeJS*, *Python*, and *Ruby*.

We test these benchmarks with `1.json` as the input. After creating WSK actions based on functions, you can pass this file as the input parameter of WSK CLI, similar to this:
```
wsk action invoke json-python -i -r -P ./1.json
```
You can create new JSONs by running:
```
ruby generate_json.rb
```