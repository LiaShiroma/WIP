import logging, logging.config

class InitLogger():

    def __init__ (self, build_name):        
        logging.config.fileConfig(fname='\\PROD\\conf\\logger.conf', disable_existing_loggers=False)
        self.logger = logging.getLogger(build_name)
        
    def build_logger(self):
        return self.logger