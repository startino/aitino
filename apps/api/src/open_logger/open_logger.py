import os
import errno
import logging

from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def create_handlers(log_fname=None, c_level=logging.INFO, f_level=logging.DEBUG):

    f_handler = None

    if log_fname is not None:
        # Create handlers
        f_handler = TimedRotatingFileHandler(log_fname)
        f_handler.setLevel(f_level)

        # Create formatters and add it to handlers
        f_format = logging.Formatter(
            "[%(asctime)s] {%(pathname)s:%(lineno)d} %(name)s - %(levelname)s - %(message)s"
        )

        # Apply formatter
        f_handler.setFormatter(f_format)

    # Create handler
    c_handler = logging.StreamHandler()
    c_handler.setLevel(c_level)

    # Create formatter and add it to handler
    c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    # Apply formatter
    c_handler.setFormatter(c_format)

    return c_handler, f_handler


def configure_logger(
    logger, log_to_file=False, console_level=logging.INFO, file_level=logging.DEBUG
):

    # Create log dir
    root_dir = os.path.normpath(os.getcwd() + os.sep)
    root_log_dir = root_dir
    make_sure_path_exists(os.path.join(root_log_dir, "logs"))
    log_dir = os.path.join(root_log_dir, "logs")

    now = datetime.now()

    logger.setLevel(logging.DEBUG)

    if log_to_file:
        # Create path
        make_sure_path_exists(os.path.join(log_dir, now.strftime("%Y")))
        log_year_dir = os.path.join(log_dir, now.strftime("%Y"))
        make_sure_path_exists(os.path.join(log_year_dir, now.strftime("%B")))
        log_month_dir = os.path.join(log_year_dir, now.strftime("%B"))
        make_sure_path_exists(os.path.join(log_month_dir, now.strftime("%d")))
        log_day_dir = os.path.join(log_month_dir, now.strftime("%d"))

        log_fname = os.path.join(
            log_day_dir, "{}.log".format(now.strftime("%b-%d-%Y_%H-%M-%S"))
        )

        # Create Handlers
        c_handler, f_handler = create_handlers(log_fname)
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
    else:
        c_handler, _ = create_handlers()
        logger.addHandler(c_handler)

    logging.info("logging configured")
    return logger

def configure_loggers(
    loggers, log_to_file=False, console_level=logging.INFO, file_level=logging.DEBUG
):
    for logger in loggers:
        configure_logger(logger, log_to_file, console_level, file_level)


if __name__ == "__main__":
    logger = logging.getLogger()

    configure_logger(logger)

    logging.debug(
        "Debug Test Log - Detailed information, typically of interest only when diagnosing problems."
    )
    logging.info("Info Test Log - Confirmation that things are working as expected.")
    logging.warning(
        "Warining Test Log - An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected."
    )
    logging.error(
        "Error Test Log - Due to a more serious problem, the software has not been able to perform some function."
    )
    logging.critical(
        "Critical Test Log - A serious error, indicating that the program itself may be unable to continue running."
    )


