#!/usr/bin/env python3

# Copyright (c) 2019 Princeton University, 2022 UBC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Standard imports
import json
from optparse import OptionParser
import os
import requests
from requests_futures.sessions import FuturesSession
import subprocess
import sys
import time
import threading
import logging

# Local imports
sys.path = ["./", "../"] + sys.path
from GenConfigs import *

sys.path = [FAAS_ROOT + "/synthetic_workload_invoker"] + sys.path
from EventGenerator import GenericEventGenerator
from commons.JSONConfigHelper import CheckJSONConfig, ReadJSONConfig
from commons.Logger import ScriptLogger
from WorkloadChecker import CheckWorkloadValidity

logging.captureWarnings(True)
logger = ScriptLogger("workload_invoker", "SWI.log")


param_file_cache = {}  # a cache to keep json of param files
binary_data_cache = {}  # a cache to keep binary data (image files, etc.)

base_url = []
base_gust_url = []
RESULT = "true"


def PROCESSInstanceGenerator(instance, instance_script, instance_times, blocking_cli):
    if len(instance_times) == 0:
        return False
    after_time, before_time = 0, 0

    if blocking_cli:
        pass
    else:
        instance_script = instance_script + " &"

    for t in instance_times:
        time.sleep(max(0, t - (after_time - before_time)))
        before_time = time.time()
        os.system(instance_script)
        after_time = time.time()

    return True


def HTTPInstanceGeneratorOW(action, instance_times, blocking_cli, param_file=None):
    if len(instance_times) == 0:
        return False
    session = FuturesSession(max_workers=15)
    url = base_url + action
    parameters = {"blocking": blocking_cli, "result": RESULT}
    authentication = (user_pass[0], user_pass[1])
    after_time, before_time = 0, 0

    if param_file == None:
        st = 0
        for t in instance_times:
            st = st + t - (after_time - before_time)
            before_time = time.time()
            if st > 0:
                time.sleep(st)
            future = session.post(
                url, params=parameters, auth=authentication, verify=False
            )
            after_time = time.time()
    else:  # if a parameter file is provided
        try:
            param_file_body = param_file_cache[param_file]
        except:
            with open(param_file, "r") as f:
                param_file_body = json.load(f)
                param_file_cache[param_file] = param_file_body

        for t in instance_times:
            st = t - (after_time - before_time)
            if st > 0:
                time.sleep(st)
            before_time = time.time()
            future = session.post(
                url,
                params=parameters,
                auth=authentication,
                json=param_file_body,
                verify=False,
            )
            after_time = time.time()

    return True


def BinaryDataHTTPInstanceGeneratorOW(action, instance_times, blocking_cli, data_file):
    """
    TODO: Automate content type
    """
    url = base_gust_url + action
    session = FuturesSession(max_workers=15)
    if len(instance_times) == 0:
        return False
    after_time, before_time = 0, 0

    try:
        data = binary_data_cache[data_file]
    except:
        data = open(data_file, "rb").read()
        binary_data_cache[data_file] = data

    for t in instance_times:
        st = t - (after_time - before_time)
        if st > 0:
            time.sleep(st)
        before_time = time.time()
        session.post(
            url=url,
            headers={"Content-Type": "image/jpeg"},
            params={"blocking": blocking_cli, "result": RESULT},
            data=data,
            auth=(user_pass[0], user_pass[1]),
            verify=False,
        )
        after_time = time.time()

    return True


def HTTPInstanceGeneratorGeneric(instance_times, blocking_cli, url, data):
    if len(instance_times) == 0:
        return False

    session = FuturesSession(max_workers=100)
    parameters = {"blocking": blocking_cli, "result": RESULT}
    # authentication = (user_pass[0], user_pass[1])
    after_time, before_time = 0, 0

    st = 0
    for t in instance_times:
        st = st + t - (after_time - before_time)
        before_time = time.time()
        if st > 0:
            time.sleep(st)
        future = session.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
            verify=False,
        )
        # print(future.result().text) # this would make it blocking if used
        after_time = time.time()

    return True


def CreateActionInvocationTreads(workload, all_events):
    threads = []
    for (instance, instance_times) in all_events.items():
        blocking_cli = workload["blocking_cli"]
        if workload["endpoint"] == "local_openwhisk":
            action = workload["instances"][instance]["application"]
            try:
                param_file = workload["instances"][instance]["param_file"]
            except:
                param_file = None
            if "data_file" in workload["instances"][instance].keys():
                data_file = workload["instances"][instance]["data_file"]
                threads.append(
                    threading.Thread(
                        target=BinaryDataHTTPInstanceGeneratorOW,
                        args=[action, instance_times, blocking_cli, data_file],
                    )
                )
            else:
                threads.append(
                    threading.Thread(
                        target=HTTPInstanceGeneratorOW,
                        args=[action, instance_times, blocking_cli, param_file],
                    )
                )
        elif workload["endpoint"] == "generic":
            url = workload["instances"][instance]["url"]
            data = workload["instances"][instance]["data"]
            threads.append(
                threading.Thread(
                    target=HTTPInstanceGeneratorGeneric,
                    args=[instance_times, blocking_cli, url, data],
                )
            )
        pass

    return threads


def main(argv):
    """
    The main function.
    """
    logger.info("Workload Invoker started")
    print("Log file -> logs/SWI.log")
    parser = OptionParser()
    parser.add_option(
        "-c",
        "--config_json",
        dest="config_json",
        help="The input json config file describing the synthetic workload.",
        metavar="FILE",
    )
    (options, args) = parser.parse_args()

    if not CheckJSONConfig(options.config_json):
        logger.error("You should specify a JSON config file using -c option!")
        return False  # Abort the function if json file not valid

    workload = ReadJSONConfig(options.config_json)
    if not CheckWorkloadValidity(workload=workload):
        return False  # Abort the function if json file not valid

    [all_events, event_count] = GenericEventGenerator(workload)

    if workload["endpoint"] == "local_openwhisk":
        # building the http endpoint addresses for the local OpenWhisk deployment
        APIHOST = subprocess.check_output(
            WSK_PATH + " property get --apihost", shell=True
        ).split()[3]
        APIHOST = "https://" + APIHOST.decode("utf-8")
        AUTH_KEY = subprocess.check_output(
            WSK_PATH + " property get --auth", shell=True
        ).split()[2]
        AUTH_KEY = AUTH_KEY.decode("utf-8")
        user_pass = AUTH_KEY.split(":")
        NAMESPACE = subprocess.check_output(
            WSK_PATH + " property get --namespace", shell=True
        ).split()[2]
        NAMESPACE = NAMESPACE.decode("utf-8")
        base_url = APIHOST + "/api/v1/namespaces/" + NAMESPACE + "/actions/"
        base_gust_url = APIHOST + "/api/v1/web/guest/default/"

    threads = CreateActionInvocationTreads(workload, all_events)

    # Dump Test Metadata
    os.system(
        "date +%s%N | cut -b1-13 > "
        + FAAS_ROOT
        + "/synthetic_workload_invoker/test_metadata.out"
    )
    os.system(
        "echo "
        + options.config_json
        + " >> "
        + FAAS_ROOT
        + "/synthetic_workload_invoker/test_metadata.out"
    )
    os.system(
        "echo "
        + str(event_count)
        + " >> "
        + FAAS_ROOT
        + "/synthetic_workload_invoker/test_metadata.out"
    )

    try:
        if workload["perf_monitoring"]["runtime_script"]:
            runtime_script = (
                "bash "
                + FAAS_ROOT
                + "/"
                + workload["perf_monitoring"]["runtime_script"]
                + " "
                + str(int(workload["test_duration_in_seconds"]))
                + " &"
            )
            os.system(runtime_script)
            logger.info("Runtime monitoring script ran")
    except:
        pass

    logger.info("Test started")
    for thread in threads:
        thread.start()
    logger.info("Test ended")

    return True


if __name__ == "__main__":
    main(sys.argv)
