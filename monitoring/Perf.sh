# This script uses the linux "perf" tool to gather certain information.

sudo perf stat -a -e cpu-cycles,L1-dcache-loads,L1-dcache-load-misses,L1-icache-load-misses,dTLB-load-misses,dTLB-loads,iTLB-load-misses,iTLB-loads,branch-misses,context-switches,cpu-migrations,page-faults -I $2 -o perf-mon.out sleep $1