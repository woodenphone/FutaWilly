# store_and_load.py
# Interact with our data-store
# =====
# Imports
# stdlib
import os
import logging
# Remote libraries
# Local modules
import common
import config.store_and_load_config as config



def compare_posts(post_a, post_b):
    """Return whether two posts are the same."""
    # Check post id
    if (post_a['num'] != post_b['num']):
        return False
    # Check last modified date
    if (post_a['timestamp'] != post_b['timestamp']):
        return False
    # If no differences, return True
    return True


def update_thread(thread, thread_num):
    """High-level
    Save any new posts to the DB"""
    pass# TODO


def read_thread(thread_num):
    """High-level
    Retreive thread data from storage"""
    pass# TODO


def ll_store_thread(thread):
    """Low-Level, use caution!
    Directly read the thread data that exists in storage"""
    pass# TODO


def ll_load_thread(thread_num):
    """Low-Level, use caution!
    Write the given thread data directly to storage"""
    pass# TODO




def main():
    pass
if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "store_and_load.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception as e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")