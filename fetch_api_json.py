# fetch_api_json.py
# Get JSON from the API
# =====
# Imports
# stdlib
import os
import logging
# Remote libraries
# Custom versions of remote libraries
print('os.getcwd()={0!r}'.format(os.getcwd()))
import py8chan_local_branch.py8chan.__init__ as py8chan
# Local modules
import common
import config_fetch_api_json as config






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






