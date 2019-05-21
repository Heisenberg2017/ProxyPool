#!/usr/bin/env python
# coding = utf-8
# Created by carey at 4/30/19
import logging
import os
from logging.handlers import RotatingFileHandler
from proxypool import settings


class EmptyHandler(logging.Handler):
    def __init__(self):
        self.lock = None
        self.level = 0
        super(EmptyHandler, self).__init__()

    def emit(self, record):
        pass

    def handle(self, record):
        pass

    def createLock(self):
        self.lock = None


class Logger(object):
    def __init__(self, logging_enable, log_name, log_level, logger_name):
        self.logger = logging.getLogger(logger_name)
        if logging_enable:
            logger_level_upper = log_level.upper()
            logger_level_obj = getattr(logging, logger_level_upper, logging.ERROR)

            # handler1: logging to file
            backup_count = 5
            logfile = os.path.join(os.getcwd(), "log")
            try:
                os.mkdir(logfile)
            except FileExistsError:
                pass
            logfile = os.path.join(logfile, log_name + ".log")
            max_log_size = 100 * 1024 * 1024  # Unit: Bytes ==  100 MB
            file_handler = RotatingFileHandler(
                logfile, mode='a', maxBytes=max_log_size, backupCount=backup_count
            )
            format_ = "%(asctime)-15s %(levelname)-8s [%(filename)s:%(lineno)d(%(funcName)s)] %(message)s"
            formatter = logging.Formatter(format_)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            # default logging is ERROR if log_level was not support
            file_handler.setLevel(logger_level_obj)
            self.logger.setLevel(logger_level_obj)

            if "DEBUG" == logger_level_upper:
                # handler2: console handler -- only for DEBUG mode
                ch = logging.StreamHandler()
                # ch.setLevel(logger_level_obj)
                ch.setFormatter(formatter)
                self.logger.addHandler(ch)
                self.logger.removeHandler(file_handler)
        else:
            self.logger.addHandler(EmptyHandler())
        self.logger.propagate = False

    def get_logger(self):
        return self.logger


logger_factory = Logger(settings.LOGGING_ENABLE, 'spider', settings.LOGGING_LEVEL, 'spider')
logger = logger_factory.get_logger()