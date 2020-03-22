import inspect
import json
import logging
import logging.handlers
import logging.config
import os

from app import ROOT_DIR
from app.utils.file_utils import get_parent_folder

default_fmt = "[%(asctime)s][%(levelname)s][%(name)s][%(module)s]: %(message)s"
default_datefmt = "%Y-%m-%d %H:%M:%S"


def get_log_level_from_str(log_level_str):
    if log_level_str.upper() == "DEBUG":
        return logging.DEBUG
    elif log_level_str.upper() == "INFO":
        return logging.DEBUG
    elif log_level_str.upper() in ["WARNING", "WARN"]:
        return logging.WARNING
    elif log_level_str.upper() == "ERROR":
        return logging.ERROR
    elif log_level_str.upper() == "CRITICAL":
        return logging.CRITICAL
    else:
        return logging.DEBUG


def get_logger(log_config_path='config.json', start_from_root_path=False, logger_name=None):
    frame = inspect.stack()[1][0]
    called_module = inspect.getmodule(frame)
    parent_folder = get_parent_folder(called_module.__file__)
    path = os.path.join(ROOT_DIR, log_config_path) if start_from_root_path else os.path.join(parent_folder,
                                                                                             log_config_path)
    if not os.path.exists(path):
        raise FileExistsError(
            "Logging config file not found at " + path + " | start_from_root_path: " + str(start_from_root_path))
        # return logging.getLogger()

    with open(path, 'rt') as file:
        lines = file.read()
        config = json.loads(lines)

    logging.config.dictConfig(config)
    if 'loggers' in config and config['loggers']:
        log = logging.getLogger(next(iter(config['loggers'])) if logger_name is None else logger_name)
    else:
        log = logging.getLogger()
    # Checking user-defined loggers
    if 'user_defined' in config and config['user_defined']:
        user_defined = config['user_defined']
        for handler_name, kwargs in user_defined.items():
            class_name = kwargs.pop('class')
            if class_name == "TimedRotatingFileHandler":
                level = get_log_level_from_str(kwargs.pop('level') if 'level' in kwargs else "DEBUG")
                formatter = logging.Formatter(fmt=kwargs.pop('fmt') if 'level' in kwargs else default_fmt,
                                              datefmt=kwargs.pop('datefmt') if 'level' in kwargs else default_datefmt)

                log_filename = kwargs['filename']
                log_folder = get_parent_folder(log_filename)
                joint_folder = os.path.join(parent_folder, log_folder)
                kwargs['filename'] = os.path.join(parent_folder, log_filename)
                os.makedirs(joint_folder, exist_ok=True)

                handler = logging.handlers.TimedRotatingFileHandler(**kwargs)
                handler.setLevel(level)
                handler.setFormatter(formatter)

                log.addHandler(handler)
    return log


def get_logger_handler(logger, handler_types):
    if logger.handlers:
        for handler in logger.handlers:
            if type(handler) in handler_types:
                return handler


def write_process_pid(module_name):
    with open(module_name + '.pid', 'wt') as pidfile:
        pidfile.write(str(os.getpid()))
