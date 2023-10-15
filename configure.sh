# This script sets some universal parameters.
# It should be run oly once.

# Installing basic dependencies if needed
sudo apt-get install -y moreutils

# Check if python3.10 is installed
if ! command -v python3.10 &> /dev/null
then
    echo "Python 3.10 could not be found. Installing..."
    sudo apt-get install -y software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install -y python3.10
else
    echo "Python 3.10 is already installed."
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "Pip could not be found. Installing..."
    sudo apt-get install -y python3-pip
else
    echo "Pip is already installed."
fi

# Install python dependencies
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
