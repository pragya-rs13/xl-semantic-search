from logging import getLogger, INFO, Formatter
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name):
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, "app.log")

    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    logger = getLogger(name)
    logger.setLevel(INFO)
    handler.setLevel(INFO)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logger("semantic_search")