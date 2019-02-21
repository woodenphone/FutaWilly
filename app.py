# webapp.py
# FLASK webapp playground
#
# =====
# Imports
# stdlib
import os
import logging
# Remote libraries
import flask
# Local modules
import common
import config.webapp_config as config






def main():
    pass


if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "webapp.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception as e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")

