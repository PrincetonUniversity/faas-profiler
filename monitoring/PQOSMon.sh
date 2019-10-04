# This script uses the Intel(R) RDT Software Package to monitor LLC occupation, 
# LLC misses, memory bandwidth, and IPC for different cores.
# For package installation and/or checking the compatibility, check this GitHub repo:
# https://github.com/intel/intel-cmt-cat

sudo pqos-msr -t $1 -o pqos-msr-mon.out -i $2