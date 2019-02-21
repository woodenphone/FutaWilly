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
import common
import config.fetch_api_json_config as config






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



all_boards = py8chan.get_all_boards()

logging.debug('all_boards={0!r}'.format(all_boards))






