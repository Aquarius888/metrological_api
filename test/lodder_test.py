import os
import logging
from logging.handlers import RotatingFileHandler


def configure_logging():
    logger = logging.getLogger(__name__)
    logger.level = 1
    format_str = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt=format_str)

    script_name = os.path.basename(__file__).split(".")[0]
    log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '{0}.log'.format(script_name))
    rotating_hndlr = RotatingFileHandler(filename=log_path, maxBytes=5*1024*1024, backupCount=2)
    rotating_hndlr.setFormatter(formatter)
    logger.addHandler(rotating_hndlr)

    return logger


def logger_test():
    return 'test test test'


#configure_logging().level = 1
#configure_logging().warning('Run')
#print(logger_test())
configure_logging().debug(logger_test())


# import logging
#
# logging.basicConfig(filename="sample.log", level=logging.INFO)
# log = logging.getLogger("ex")
#
# log.debug('test log')
# try:
#     raise RuntimeError
# except RuntimeError:
#     log.exception("Error!")
