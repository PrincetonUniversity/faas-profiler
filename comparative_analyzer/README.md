# Comparative Analyzer

This module compares the results of tests stores as pickle files in the `../data_archive` directory.

## How to use Comparative Analyzer
1. Make sure that you have ran your test(s) with **Synthetic Workload Invoker**  and analyzed them with **Workload Analyzer** with `-a` option to store archive(s).
2. Then run the Comparative Analyzer:
```
python ComparativeAnalyzer.py
```
3. Certain features can be controlled by input arguments:
    1. `-s` or `--since`: you can specify a timestamp that only archives after that should be included.
    2. `-p` or `--plot`: plotting default comperative results.
    3. `-c` or `--customized_plot=FILE`: use a customized plotting script. This customized script should include the function `ComparativePlotting`. Look at the script `CustomPlotting.py` as an example.
4. Logs can be found in `../logs/CA.log`.
