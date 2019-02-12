#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, time, os, logging
import inspect

## Create a logger
# @param logfilename
# @param loglevel
# @return logging handle
def create_logger(logfilename, loglevel):
    logger = logging.getLogger('keepnote')
    logger.setLevel(loglevel)
    logger.propagate = 0

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(threadName)-12s - %(levelname)-8s : %(message)s')

    # create file handler (fh)
    fh = logging.FileHandler(logfilename)
    fh.setLevel(logging.DEBUG)        # set logging level for handler
    fh.setFormatter(formatter)    # add formatter to handler
    logger.addHandler(fh)            # add handler to logger

    # create console handler (ch)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Logfile = " + logfilename)
    date = time.strftime("%d/%m/%Y - %H:%M:%S")
    logger.info("Date = " + date)
    return logger



def msg_whoami():
    import inspect
    msg = "line %d in %s %s" % (inspect.currentframe().f_lineno, \
                                    str(inspect.currentframe().f_code.co_name), \
                                    str(inspect.currentframe().f_locals['self']))
    return msg
                                    


