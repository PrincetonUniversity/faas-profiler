# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import datetime
import logging
import os
import sys

# Local imports
sys.path = ['./', '../'] + sys.path
from GenConfigs import *
sys.path = [FAAS_ROOT + '/synthetic_workload_invoker'] + sys.path
from commons.Logger import ScriptLogger

logger_wlch = ScriptLogger('workload_checker', 'SWI.log')

supported_distributions = {'Poisson', 'Uniform'}

def CheckWorkloadValidity(workload):
    """
    Checks whether a loaded workload is valid.
    """
    logger_wlch.info("Started CheckWorkloadValidity")
    # 1 - Check if the workload has been successfully read in ReadJSONConfig
    if workload is None:
        logger_wlch.info('Workload not valid => Terminating')
        return False
    # 2 - Check for validity of general field
    print(workload)
    fields_to_check = [['test_name', str], ['blocking_cli', bool]]
    for field in fields_to_check:
        try:
            print([field, workload[field[0]]])
            if type(workload[field[0]]) is not field[1]:
                test_name('Input of the ' +
                          field[0] + ' field should be a ' + str(field[1]))
                return False
        except:
            logger_wlch.error('No ' + field[0] + ' field provided!')
            return False
    # # 3 - Check if invocation scripts exists for all functions/applications in the workload
    application_set = set()
    distribution_set = set()
    for (instance, specs) in workload['instances'].items():
        application_set.add(specs['application'])
        try:
            distribution_set.add(specs['distribution'])
        except:
            pass

    logger_wlch.info('Required applications: ' + str(application_set))
    # 4 - Check for supported distributions
    if not distribution_set.issubset(supported_distributions):
        logger_wlch.error(
            'At least one specified distribution is not supported. Supported distribution(s): '+str(supported_distributions))
        return False
    # 5 - Check for valid test duration
    try:
        test_duration_in_seconds = workload['test_duration_in_seconds']
        if test_duration_in_seconds is None:
            logger_wlch.error(
                'Please enter a valid value for test_duration_in_seconds field in the config file.')
            return False
        elif int(test_duration_in_seconds) <= 0:
            logger_wlch.error(
                'test_duration_in_seconds should be greater than zero!')
            return False
    except:
        logger_wlch.error(
            'test_duration_in_seconds field not specified in the json config file')
        return False
    # 6 - Check that the random_seed field is entered
    try:
        random_seed = workload['random_seed']
    except:
        logger_wlch.error("No random_seed field specified in the config file")
        return False

    return True
