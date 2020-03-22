import time

from app.api.module import log
from app.api.module import module_1, module_2


def main():
    while True:
        time.sleep(1)
        log.info('INFO')
        module_1.func()
        module_2.func()


if __name__ == '__main__':
    # with daemon.DaemonContext():
    main()
