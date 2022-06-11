import sys
import logging

class logger:
    def __init__(self,name,level,):
        self.version = "1.0.0"
        if level.casefold() == "notset".casefold():
            level = logging.NOTSET
        elif level.casefold() == "debug".casefold():
            level = logging.DEBUG
        elif level.casefold() == "info".casefold():
            level = logging.INFO
        elif level.casefold() == "warn".casefold():
            level = logging.WARNING
        elif level.casefold() == "error".casefold():
            level = logging.ERROR
        elif level.casefold() == "critical".casefold():
            level = logging.CRITICAL
        self.logger = logging.getLogger(str(name))
        sh = logging.StreamHandler(sys.stdout)
        self.logger.setLevel(level)
        fmt = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]%(message)s", "%Y-%m-%d %H:%M:%S")
        sh.setFormatter(fmt)
        self.logger.addHandler(sh)
    def debug(self,string):
        self.logger.debug(str(string))
    def info(self,string):
        self.logger.info(str(string))
    def warning(self,string):
        self.logger.warning(str(string))
    def error(self,string):
        self.logger.error(str(string))
    def critical(self,string):
        self.logger.critical(str(string))
