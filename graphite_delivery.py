import graphitesend
import time
import sys
import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

sys.path.append('.')
import settings


graphitesend.init(
    init_type='plaintext_tcp',
    graphite_server=settings.CARBON_SERVER,
    graphite_port=settings.CARBON_PORT,
    prefix=settings.CARBON_PREFIX,
    suffix=settings.CARBON_SUFFIX,
    system_name=settings.CARBON_SYSTEM,
)

current_timestamp = int(time.time())


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


def send_data(data, country_acr, prefix, message_postfix, api_type):
    """Send received data to carbon

    :param data: response of Metrological API in json
    :param country_acr: country acronym
    :param prefix: message prefix
    :param message_postfix: message postfix
    :param api_type: type of api (section)
    :return: pass
    """
    if api_type == 'widget':
        categories = data["data"][country_acr]["categories"]
        data_type = data["data"][country_acr]["data"]

        for i in range(0, len(categories)):
            tmp = categories[i] / 1000 + settings.TIME_SHIFT
            message = prefix + message_postfix
            configure_logging().info((message, data_type[i], datetime.datetime.fromtimestamp(tmp).isoformat()))
            graphitesend.send(
                metric=message,
                value=data_type[i],
                timestamp=tmp,
            )
    else:
        avg = data["avg"]

        message = prefix + message_postfix
        configure_logging().info((message, avg, datetime.datetime.fromtimestamp(current_timestamp).isoformat()))
        graphitesend.send(
            metric=message,
            value=avg,
            timestamp=current_timestamp,
            )

