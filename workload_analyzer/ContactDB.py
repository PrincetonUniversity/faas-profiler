# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import os
from wskutil import request
import sys

sys.path = ['./', '../'] + sys.path

# Local
from GenConfigs import *

DB_CONFIG_FILE = os.path.expanduser(
    WSK_PATH[:-3]+'/../ansible/db_local.ini')

# Examples:
# print(GetDBConfigs())
# print(GetActivation(activation_id='e107e05a84cf469c87e05a84cf669c16', namespace='guest'))
# print(GetActivationRecordsSince(1536032293317, 100))
# print(GetActivationIDsSince(1536032293317, 100))


def GetDBConfigs():
    """
    Retrieves DB configs from a configuration file.
    """
    configs = {}
    with open(DB_CONFIG_FILE, 'r') as config_file:
        lines = config_file.readlines()
        for line in lines:
            if line[0] == '[':
                domain = line[1:-2]
                configs[domain] = {}
                last_dom = domain
            else:
                try:
                    key = line[:line.index('=')]
                except:
                    continue
                configs[last_dom][key] = line[line.index('=')+1:-1]

    return configs['db_creds']


def GetAllActivationDocs():
    """
    Returns all activation record keys.
    """
    configs = GetDBConfigs()
    url = configs['db_protocol']+'://'+configs['db_host']+':' + \
        configs['db_port']+'/'+'whisk_local_activations/_all_docs'
    headers = {
        'Content-Type': 'application/json',
    }
    res = request('GET', url, headers=headers, auth='%s:%s' %
                  (configs['db_username'], configs['db_password']))

    return json.loads(res.read())


def GetActivationRecordsSince(since, limit=100):
    """
    Returns details on activation records since a given tick in milliseconds
    """
    configs = GetDBConfigs()
    url = configs['db_protocol']+'://'+configs['db_host']+':' + \
        configs['db_port']+'/'+'whisk_local_activations/_find'
    headers = {
        'Content-Type': 'application/json',
    }
    body = {
        "selector": {
            "start": {
                "$gte": since
            }
        },
        "limit": limit
    }

    res = request('POST', url, body=json.dumps(body), headers=headers,
                  auth='%s:%s' % (configs['db_username'], configs['db_password']))

    return json.loads(res.read())


def GetActivationIDsSince(since, limit=100):
    """
    Returns the activation IDs (including the namespace)
    """
    configs = GetDBConfigs()
    url = configs['db_protocol']+'://'+configs['db_host']+':' + \
        configs['db_port']+'/'+'whisk_local_activations/_find'
    headers = {
        'Content-Type': 'application/json',
    }
    body = {
        "selector": {
            "start": {
                "$gte": since
            }
        },
        "limit": limit
    }
    res = request('POST', url, body=json.dumps(body), headers=headers,
                  auth='%s:%s' % (configs['db_username'], configs['db_password']))
    doc = json.loads(res.read())
    IDs = [x['_id'] for x in doc["docs"]]

    return IDs


def GetActivation(activation_id, namespace='guest'):
    """
    Returns details for an activation id.
    """
    configs = GetDBConfigs()
    url = configs['db_protocol']+'://'+configs['db_host']+':'+configs['db_port'] + \
        '/'+'whisk_local_activations'+'/'+namespace+'%2F'+activation_id
    headers = {
        'Content-Type': 'application/json',
    }
    res = request('GET', url, headers=headers, auth='%s:%s' %
                  (configs['db_username'], configs['db_password']))

    return json.loads(res.read())
