# This script sets some universal parameters.
# It should be run oly once.

# Installing some dependencies if needed
sudo apt-get install -y moreutils
python3.10 -m pip install -r requirements.txt

# Configure path variables used by the platform 
ROOTLINE='FAAS_ROOT="'$(echo $PWD)'"'
echo $ROOTLINE >> GenConfigs.py
echo 'WSK_PATH = "'$(which wsk)'"' >> GenConfigs.py

# Configure root path
echo $ROOTLINE | cat - invocation-scripts/monitoring.sh | sponge invocation-scripts/monitoring.sh
echo $ROOTLINE | cat - monitoring/RuntimeMonitoring.sh | sponge monitoring/RuntimeMonitoring.sh

# Make local directories
if [ -d "logs" ]
then
    echo "Directory logs already exists."
else
    mkdir logs
fi
if [ -d "data_archive" ]
then
    echo "Directory data_archive already exists."
else
    mkdir data_archive
fi
