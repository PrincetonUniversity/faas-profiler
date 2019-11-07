# This script uses the Linux "perf" tool to gather certain information.

# Notes:
# 1. The events listed below are just some of the examples. You can find the full list of events by running `perf list`.
# 2. It is usually recommended to go for fewer events to ensure low profiling overhead.

sudo perf stat -a -e cpu-cycles,L1-dcache-loads,L1-dcache-load-misses,L1-icache-load-misses,dTLB-load-misses,dTLB-loads,iTLB-load-misses,iTLB-loads,branch-misses,context-switches,cpu-migrations,page-faults -I $2 -o perf-mon.out sleep $1
