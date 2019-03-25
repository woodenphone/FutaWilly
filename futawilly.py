#-------------------------------------------------------------------------------
# Name:        futawilly.py
# Purpose:
#
# Author:      Ctrl-S
#
# Created:     26-03-2019
# Copyright:   (c) Ctrl-S 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Imports
# stdlib
import os
import logging
# Remote libraries
import flask
import py8chan
# Local modules
import common
import config.futawilly_config as config




def main():
    pass


if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "futawilly.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception as e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")

# ===== ===== ===== =====
# Functions


# ===== ===== ===== =====
# Okay, let's pseudocode up the basic event loop
# DEFINE current_threads AS local memory copy of threads, 'current' state that gets updated by 'new' remote data
current_threads = {}


# Initialize state
board = py8chan.Board(board_name=config.board_name)

# Load live threads list from DB?



logging.debug('Starting to update threads')
# Update from remote server
# Threads list
threads = board.get_all_threads()

# Check each thread that was listed against what we have.
# - If new.latest_post > local.latest_post: reprocess thread. Otherwise thread is unchanged.
for thread in threads:
    do_thread_update = False# Should this thread be updated this cycle?
    # Is thread updated?
    # Compare last post number
    thread_number = thread.num
    try:
        current_thread = current_threads[thread_number]
    except Keyerror:
        # Thread is new
        # Initialize local version
        current_thread = {}
        current_threads[thread_number] = current_thread# Reference the same object in memory
        # Update thread
        do_thread_update = True

    # Compare the last post of each version of the thread against each other
    if thread.replies[-1].post_id != current_thread.replies[-1].post_id:
        logging.debug('New post detected in thread')
        do_thread_update = True


    if do_thread_update:
        # Updated threads
        # Store new version of thread
        logging.debug('Updating thread {0}'.format(thread.num))

logging.debug('Finished updating threads')











# ===== ===== ===== =====
# Perseistant data store
# Postgres is desired. JSONB was requested as post storage datatype.
# sqlite is stdlib though, so let's prototype with that.

# Use a ORM so we don't have to learn SQL. We only want to use the DB as a big datastore that won't rape our HDD with millions of files.
# SQLAlchemy

# Table names
#
# v_threads
# v_media
#

# Board-level threads table. One row per thread.
# v_threads
# primary_key, thread_num, op_num, last_reply_num, updated_timestamp, deleted_timestamp


# Roard-level media table, map image_id to image_hash to filepath.
# v_media
# primary_key, size_bytes, image_id, md5b64, sha1b64, path_fullview, path_opthumb, path_replythumb,
def give_img_table(board_name):
    class BoardMedia:

# ===== ===== ===== =====
