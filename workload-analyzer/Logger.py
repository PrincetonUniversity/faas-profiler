# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging


def ScriptLogger(loggername, filename):
    """
    This function logs the scripts.
    """
    # create logger
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    lfh = logging.FileHandler(filename)
    lfh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    lch = logging.StreamHandler()
    lch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    lfh.setFormatter(formatter)
    lch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(lfh)
    logger.addHandler(lch)
    return logger
