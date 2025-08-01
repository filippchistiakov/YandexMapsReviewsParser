import logging
import sys
from typing import Optional


def configure_logging(
        debug: bool = False,
        log_file: Optional[str] = None
) -> None:
    # '%(asctime)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    # '%(asctime)s [%(levelname)s] %(module)s:%(funcName)s:%(lineno)d - %(message)s'

    logging.getLogger().handlers.clear()
    fmt_str = '%(asctime)s %(levelname)s %(name)s {%(filename)s:%(lineno)d}  - %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.addFilter(lambda rec: rec.levelno <= logging.INFO)
    formatter_info = logging.Formatter(
        fmt=fmt_str,
        datefmt=datefmt,
    )
    stdout_handler.setFormatter(formatter_info)

    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.addFilter(lambda rec: rec.levelno > logging.INFO)
    formatter_warnings = logging.Formatter(
        fmt=fmt_str,
        datefmt=datefmt,
    )
    stderr_handler.setFormatter(formatter_warnings)

    logging.getLogger().addHandler(stdout_handler)
    logging.getLogger().addHandler(stderr_handler)
    logging.getLogger().setLevel(logging.INFO)
    if debug:
        logging.getLogger('parser').setLevel(logging.DEBUG)

    logging.info(f'Logging configured successfully')
    logging.debug('Debug logging is enabled')
    logging.warning('This is a warning message')
