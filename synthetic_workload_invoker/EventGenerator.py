# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
import numpy as np
import random

from commons.Logger import ScriptLogger

logger_eg = ScriptLogger("event_generator", "SWI.log")


def CreateEvents(instance, dist, rate, duration, seed=None):
    """
    Creates a dictionary of application instances
    """
    inter_arrivals = []

    if (rate <= 0) or (duration <= 0):
        return inter_arrivals

    if dist == "Uniform":
        random.seed(seed + hash(instance))
        shift = random.random() / rate
        inter_arrivals = int(duration * rate) * [1.0 / rate]
        inter_arrivals[0] += shift
    elif dist == "Poisson":
        np.random.seed(seed)
        beta = 1.0 / rate
        oversampling_factor = 2
        # later the EnforceActivityWindow function
        # will cut out of bound samples.
        # Creating inter arrival times using an Exponential process
        inter_arrivals = list(
            np.random.exponential(
                scale=beta, size=int(oversampling_factor * duration * rate)
            )
        )

    return inter_arrivals


def EnforceActivityWindow(start_time, end_time, IATs):
    """
    This function enforces possible activity windows defined in the config file.
    """
    events_iats = []

    # Calculating absolute event times
    event_times = np.cumsum(IATs, dtype=np.float64)

    # Filter event times within the activity window
    valid_event_times = event_times[
        (event_times > start_time) & (event_times < end_time)
    ]

    if len(valid_event_times) == 0:
        return events_iats

    # Calculate inter-arrival times from filtered event times
    events_iats = [valid_event_times[0]] + np.diff(valid_event_times).tolist()

    return events_iats


def GenericEventGenerator(workload):
    """
    This function returns a list of times and applications calls given a workload description.
    """
    logger_eg.info("Started Generic Event Generator")
    test_duration_in_seconds = workload["test_duration_in_seconds"]

    all_events = {}
    event_count = 0

    random_seed = workload["random_seed"]
    logger_eg.info("random_seed: " + str(random_seed))

    for instance, desc in workload["instances"].items():
        if "interarrivals_list" in desc.keys():
            IATs = desc["interarrivals_list"]
            logger_eg.info("Read the invocation time trace for " + instance)
            # enforcing maximum test duration
            list_len = 0
            cutoff_index = None
            for i in range(len(IATs)):
                list_len += IATs[i]
                if list_len > test_duration_in_seconds:
                    cutoff_index = i
                    break
            if cutoff_index is not None:
                IATs = IATs[:cutoff_index]
        else:
            IATs = CreateEvents(
                instance=instance,
                dist=desc["distribution"],
                rate=desc["rate"],
                duration=test_duration_in_seconds,
                seed=random_seed,
            )
            if "activity_window" in desc.keys():
                if len(desc["activity_window"]) != 2:
                    msg = "activity_window should be a list with length of 2."
                    print(msg)
                    logger_eg.info(msg)
                    return [None, None]
                start_time = desc["activity_window"][0]
                end_time = desc["activity_window"][1]
                IATs = EnforceActivityWindow(start_time, end_time, IATs)
            else:
                IATs = EnforceActivityWindow(
                    0, workload["test_duration_in_seconds"], IATs
                )
        all_events[instance] = IATs
        event_count += len(IATs)

    logger_eg.info("Returning workload event list")

    return [all_events, event_count]
