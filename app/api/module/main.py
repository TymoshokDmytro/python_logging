import time
from logging.handlers import TimedRotatingFileHandler

from app.api.module import log
from app.api.module import module_1, module_2
from app.utils.logging_utils import get_logger_handler, write_process_pid


def main():
    while True:
        time.sleep(1)
        log.info('INFO')
        module_1.func()
        module_2.func()


if __name__ == '__main__':
    # with daemon.DaemonContext(files_preserve=get_logger_handler(log, [TimedRotatingFileHandler]).stream):
        write_process_pid(__name__)
        main()
