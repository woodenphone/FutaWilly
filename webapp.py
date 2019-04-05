#! /usr/bin/python3
# webapp.py
# FLASK webapp playground
#
# =====
# Imports
# stdlib
import os
import logging
# Remote libraries
from flask import Flask, url_for
from flask import request
# Local modules
import common
import config.webapp_config as config



app = Flask(__name__)


@app.route('/')
def hello_world():
    """Test that we can access pages to start with"""
    return 'Hello, World.'



@app.route('/view_thread/<board_name>/<thread_num>')
def view_thread(board_name, thread_num):
    """Display one thread."""
    resp_data = ''
    posts = None# TODO: Load posts from DB
    for post in posts:
        resp_data += ''.format()
    return 'TODO'




def main():
    app.run()


if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "webapp.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception as e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")

