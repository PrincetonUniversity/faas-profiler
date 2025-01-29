import json
import matplotlib.pyplot as plt
import os
import sys
import time

test_rates = [1000, 2000, 5000]


def ParseLog(log_file):
    with open(log_file, "r") as f:
        lines = f.readlines()

    start_time = 0
    end_time = 0
    lag = 0

    for line in lines:
        if "Test started" in line:
            start_time = line.split(" - w")[0]
            ms = int(start_time.split(",")[1])
            start_time = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S,%f"))
            start_time += ms / 1000
        if "Test ended" in line:
            end_time = line.split(" - w")[0]
            ms = int(end_time.split(",")[1])
            end_time = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S,%f"))
            end_time += ms / 1000
        if "fell behind" in line:
            lag = float(line.split("behind ")[1].split(" nanoseconds")[0])

    logged_duration = end_time - start_time
    return (logged_duration, lag)


def main():

    results = {"test_rates": [], "durations": [], "logged_durations": [], "lag": []}

    with open(
        os.path.join(
            os.path.dirname(__file__), "..", "test_data", "stress_test_workload.json"
        )
    ) as f:
        workload = json.load(f)

    for test_rate in test_rates:
        if os.path.exists(
            os.path.join(os.path.dirname(__file__), "..", "..", "logs", "SWI.log")
        ):
            os.remove(
                os.path.join(os.path.dirname(__file__), "..", "..", "logs", "SWI.log")
            )

        workload["instances"]["instance1"]["rate"] = test_rate
        file_description = "stress_test_workload_" + str(test_rate) + ".json"

        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "test_data", file_description
            ),
            "w",
        ) as f:
            json.dump(workload, f, indent=4)

        start = time.time()
        os.system(
            " cd ../../; ./WorkloadInvoker -c ./tests/test_data/" + file_description
        )
        end = time.time()

        time.sleep(0.5)

        (logged_duration, lag) = ParseLog(
            os.path.join(os.path.dirname(__file__), "..", "..", "logs", "SWI.log")
        )

        results["test_rates"].append(test_rate)
        results["durations"].append(end - start)
        results["logged_durations"].append(logged_duration)
        results["lag"].append(lag)

    with open(
        os.path.join(os.path.dirname(__file__), "stress_test_results.json"),
        "w",
    ) as f:
        json.dump(results, f, indent=4)


def plot_results():
    with open(
        os.path.join(os.path.dirname(__file__), "stress_test_results.json"),
        "r",
    ) as f:
        results = json.load(f)

    plt.plot(
        results["test_rates"], [15.0 / x for x in results["durations"]], label="Now"
    )
    plt.xlabel("Traffic Rate (rps)")
    plt.ylabel("Testing Capacity")
    plt.legend()
    plt.xscale("log")
    plt.ylim(0, 1.1)
    plt.savefig(os.path.join(os.path.dirname(__file__), "stress_test_results.png"))


if __name__ == "__main__":
    main()
