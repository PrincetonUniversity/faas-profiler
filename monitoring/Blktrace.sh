# This script uses blktrace which "generate traces of the i/o traffic on block devices" [from manual].

sudo blktrace -d /dev/sdb -w $1 -o - | blkparse -i - > blktrace-mon.out