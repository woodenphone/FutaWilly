#! /usr/bin/python3
# Expects python 3.x
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
import json
import datetime
# Remote libraries
#import flask
import sqlalchemy
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

def cusassert(assert_expression, value):
    """Custom Assert function.
    Basically assert() except should dump information about value.
    """
    if assert_expression:
        # Assertion was correct
        return
    else:
        # Assertion failed
        logging.error('ASSERT FIRED WITH VALUE: {0!r}'.format(value))
        raise AssertionError()


def generate_media_filepath(base_path, media_type, filename):
    a = filename[0:1]
    b = filename[1:4]
    filepath = os.path.join(base_path, media_type, a, b, filename)
    return filepath


def save_media_file(req_ses, base_path, media_type, url, filename):
    """Save a file to the media dir."""
    filepath = generate_media_filepath(base_path=base_path, media_type=media_type, filename=filename)
    # Load remote file into RAM
    # TODO WRITEME

    # Save data to disk
    # TODO WRITEME
    return


def save_post_media(db_ses, req_ses, base_path, boardname, post):
    """Save media from a post, adding it to the DB"""
    # TODO WRITEME
    pass


def list_db_row_post_ids(posts):
    """Takes posts field from Dd. Returns unsorted list of post numbers"""
    post_nums = []
    for post in posts:
        if post['post']:# TODO FIX THIS; TODO WRITEME
            pass# TODO FIX THIS; TODO WRITEME
        pass# TODO FIX THIS; TODO WRITEME
    pass# TODO FIX THIS; TODO WRITEME


def update_thread( db_ses, req_ses, thread, ):
    """Insert new post information to a thread's entry in the DB.
    If the thread is not already in the DB, add it."""
    # TODO WRITEME

    thread_num = thread.num
    cusassert( (type(thread_num) is unicode), value=thread_num)

    # Load DB row for thread. (or at least try to.)
    thread_find_query = session.query(Thread)\
    .filter(Thread.thread_num == thread_num)
    thread_row = thread_find_query.first()

    if not thread_row:
        # Thread is new and needs a row created.
        logging.info('Creating row for new thread: {0!r}'.format(thread_num))
        # TODO WRITEME!

    # Grab the existing thread data
    all_thread_posts = thread_row.posts
    logging.debug('all_thread_posts={0!r}'.format(all_thread_posts))

    # Isolate new posts
    local_post_ids
    remote_post_ids


    # Save any new media.

    # Change the DB row.
    thread_row.posts = new_posts_value

    logging.debug('Committing new version of thread to DB')
    session.commit()
    logging.debug('Finished updating thread {0!r}'.format(thread_num))
    return





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

### Board-level threads table. One row per thread.
### v_threads
### primary_key, thread_num, op_num, last_reply_num, updated_timestamp, deleted_timestamp
##
##
### Roard-level media table, map image_id to image_hash to filepath.
### v_media
### primary_key, size_bytes, image_id, md5b64, sha1b64, path_fullview, path_opthumb, path_replythumb,
##def give_img_table(board_name, sqlalchemy_base_thing):
##    class BoardMedia:
##        pass
##    return BoardMedia




# ===== ===== ===== =====
# Define DB
# Startup ORM mapping base thingy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Thread(Base):
    """This table is for any and all posts for this board"""
    __tablename__ = 'v_threads'# TODO FIXME: Make board-agnostic
    pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just a primary key.
    # Addressing
    thread_num = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)
    # Thread data
    posts = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)# JSON encoded posts for this thread
    first_post_num = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)# OP's post num
    last_post_num = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)# Most recent reply's post num
    # Administrative / legal compliance
    removed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Users can't access thread
    banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Fetcher can't save thread



class Image(Base):
    """This table is for any and all images/media associated with posts for this board"""
    __tablename__ = 'v_images'# TODO FIXME: Make board-agnostic
    pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just a primary key.
    # Addressing
    image_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)# Primary key?
    # Identification of image characteristics
    size_bytes = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)# Size of the fullsized image in bytes #TODO!
    hash_md5 = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# MD5 hash of full file #TODO!
    hash_sha1 = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# SHA1 hash of full file #TODO!
    hash_sha256 = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# SHA256 hash of full file #TODO!
    hash_sha512 = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# SHA512 hash of full file #TODO!
    # Files on disk
    file_extention = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# File extention of the fullview file.
    filename_full = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Fullsized media file
    filename_thumb_reply = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Thumbnail used in OP post (if applicable)
    filename_thumb_op = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Thumbnail used in reply post (if applicable)
    # Administrative / legal compliance
    removed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Users can't access file. #TODO!
    banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Fetcher can't save file #TODO!
    hard_banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Ultra-paranoid ban. Purge from cache, overwrite disk location, recheck for existance on a cronjob, the works. Use VERY sparingly. #TODO!
    refetch_needed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Resave the file if it is ever seen again. (For broken media) #TODO!
    # Hacks (Like running this shit on more than one machine per single instance. Weird use cases and such.)
    # None yet.



# ===== ===== ===== =====
# Spinup DB
logging.info('Starting DB connection...')
# SQLite3
# DB Configuration
db_filepath = os.path.join('tmp', 'futawilly.db')# For sqllite
db_connection_string = 'sqlite:///tmp/futawilly.db'

# Ensure DB path is available
db_dir = os.path.dirname(db_filepath)
logging.debug('db_dir = {0!r}'.format(db_dir))
if db_dir:# Only try to create dir if a dir is given
    if not os.path.exists(db_dir):
        logging.info('Creating DB dir: {0}'.format(db_dir))
        os.makedirs(db_dir)

### PostgreSQL
### DB Configuration
##db_connection_string = ''
# TODO WRITEME


# Start the DB engine
logging.debug('Starting DB engine.')
engine = sqlalchemy.create_engine(
    db_connection_string,# Points SQLAlchemy at a DB
    echo=True# Output DB commands to log
)
Base.metadata.create_all(engine, checkfirst=True)# Create tables based on classes. (checkfirst only creates if it doesn't exist already)


# Create a session to interact with the DB
logging.debug('Creating DB session.')
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

logging.info('DB connection established.')


# ===== ===== ===== =====
# Cache of local threads
# Initialize state
# DEFINE current_threads AS local memory copy of threads, 'current' state that gets updated by 'new' remote data
current_threads = {}
# Load initial cache of threads TODO!
# JSON file holding a relatively recent version of the threads.
json_threads_cache_filepath = config.json_threads_cache_filepath
# Ensure dir containing threads cache file exists before trying to use it.
threads_cache_dir = os.path.dirname(json_threads_cache_filepath)
if threads_cache_dir:# Only try checking for a dir if one is specified.
    if not os.path.exists(threads_cache_dir):
        os.makedirs(threads_cache_dir)

if not os.path.exists(json_threads_cache_filepath):
    logging.debug('Crating threads cache file {0}'.format(json_threads_cache_filepath))
    with open(json_threads_cache_filepath, 'wb') as new_cache_f:
        json.dump({}, new_cache_f)# Initialise as empty
# Load whatever is in the threads cache
logging.debug('Loading threads cache file {0}'.format(json_threads_cache_filepath))
with open(json_threads_cache_filepath, 'rb') as cache_f:
    local_threads = json.load(cache_f)



# A thread
example_cached_thread = {
    'thread_num': 1234,
    'posts': [
        # A post
        {
            'post_num': 1234,# Site-given post number
            'comment': 'Test OP',# Site-given comment
            'timestamp': 12345678,# Site-given timestamp
            'media': [# Images for this post
                    # An image
                    {
                    'position': 0,# Position in post display.
                    'image_id': 1,# DB lookup value.
                    'filename_long': u'example.jpg',# What the image is called in this post, including the extention.
                    'filename_short': u'example',# What the image is called in this post, excluding the extention.
                    'file_ext': u'jpg',# The file extention of the image.
                    'hash_md5': 'abcdef0123456...'# MD5 hash of this image, in case DB is fucked up.
                },
            ],
        }
    ],
    'fell_off_board': False, # Has the thread been removed by falling off the board?
    'was_deleted_early': False, # Has the thread been deleted without appearing in the archive JSONs?
    'active': True, # Is the thread still on the board?
    'deletion_timestamp': datetime.datetime(1970, 1, 1), # locally-generated? timestamp of when thread was no longer on the board
    'last_checked': datetime.datetime(1970, 1, 1),# Locally-generated date last loaded the thread.
    'last_updated': datetime.datetime(1970, 1, 1),# Locally-generated date last time a modification was made to this thread in the DB.
    'board': 'v',
}



# ===== ===== ===== =====
# Start looping over remote threads
loop_counter = 0
while (True):
    loop_counter += 1
    logging.debug('Thread check loop iteration {0}'.format(loop_counter))

    # TODO: Logic to prevent overfilling of threads cache

    # Update from remote server
    logging.debug('Starting to update threads')
    # Threads list
    board = py8chan.Board(board_name=config.board_name)
    threads = board.get_all_threads()
    print('BREAKPOINT')

    # Check each thread that was listed against what we have.
    # - If new.latest_post > local.latest_post: reprocess thread. Otherwise thread is unchanged.
    for thread in threads:
        do_thread_update = False# Should this thread be updated this cycle?
        print('BREAKPOINT')
        # Is thread updated?
        # Compare last post number
        thread_number = thread.num
        try:
            current_thread = local_threads[thread_number]
        except KeyError:
            # Thread is new
            # Initialize local version
            local_threads[thread_number] = {}
            # Update thread
            do_thread_update = True

        # Compare the last post of each version of the thread against each other
        if thread.replies[-1].post_id != current_thread.replies[-1].post_id:
            logging.debug('New post detected in thread')
            do_thread_update = True

        if do_thread_update:
            # Updated threads need updating.
            # Store new version of thread.
            logging.debug('Updating thread {0}'.format(thread.num))
            print('BREAKPOINT')
            # TODO WRITEME
            update_thread(
                db_ses=db_ses,
                req_ses=req_ses,
                thread = thread,
            )
            logging.debug('Finished updating thread {0}'.format(thread.num))

    logging.debug('Finished updating threads')
    continue



# ===== ===== ===== =====
logging.info('EOF')# End of file