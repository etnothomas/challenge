import logging


class Logger:

    @classmethod
    def get_logger(cls, logger_name):
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(format)
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger