# fetch_api_json.py
# Get JSON from the API
# =====
# Imports
# stdlib
import os
import logging
# Remote libraries
import py8chan
# Local modules
import common# common.py
import config.fetch_api_json_config as config# config/fetch_api_json_config.py


def main():
    pass

if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "fetch_api_json.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception as e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")



