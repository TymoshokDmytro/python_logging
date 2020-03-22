import inspect
import json
import logging

import logging.config
import os

from app.utils.file_utils import get_parent_folder


def get_logger(default_path='config.json', logger_name=None):
    frame = inspect.stack()[1][0]
    called_module = inspect.getmodule(frame)
    parent_folder = get_parent_folder(called_module.__file__)
    path = os.path.join(parent_folder, default_path)
    with open(path, 'rt') as file:
        lines = file.read()
        config = json.loads(lines)

    logging.config.dictConfig(config)
    log = logging.getLogger(next(iter(config['loggers'])) if logger_name is None else logger_name)
    return log


def create_time_rotating_file_handler(*args, **kwargs):
    pass
