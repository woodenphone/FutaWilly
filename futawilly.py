#! /usr/bin/python3
# Expects python 3.x
#-------------------------------------------------------------------------------
# Name:        futawilly.py
# Purpose:     Smoke weed everyday in an automated fashion on the user's behalf.
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
import copy
import hashlib
import base64
import binascii
# Remote libraries
#import flask
import sqlalchemy
import py8chan
import requests
# Local modules
import common
import config.futawilly_config as config
from fuckups import *# Local Exceptions




def main():
    pass# Literally do nothing useful.


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

def assert2(exp, msg=None, value=None):# THIS IS A DISTRACTION! LEAVE IT BE!
    """Custom Assert function.
    exp: Assert fires if not True.
    msg: Message explaining the assertion to be logged along with the value when assert fires.

    Basically assert() except should dump information about value.
    PREMISE: Trust noone, each function should verify what it gets from elsewhere just ot be fucking damn sure. This does not excuse the original data not being to spec, only excuses us from blame for propogating the fuckup.
    TODO: Make PEP for better builtin assertions; look for existing better assertions;
    """
    if exp:
        # Assertion was correct
        return None# Be fucking explicit about what we're doing.
    else:
        # Assertion failed
        logging.error('ASSERT2 FIRED WITH MESSAGE: {0}'.format(msg))
        logging.error('ASSERT2 FIRED WITH value: {0!r}'.format(value))
        raise AssertionError()


def generate_media_filepath(media_base_path, media_type, filename):
    a = filename[0:1]
    b = filename[1:4]
    filepath = os.path.join(media_base_path, media_type, a, b, filename)
    return filepath


def decide_if_media_redownload(media_base_path, board_name, image_row):
    """Logic to decide if an image seen with a post needs to be resaved.
    Used when a media row exists for the hash."""
    # Check if image needs (re)downloading
    if (image_row['banned'] == True):# Do not save banned images.
        return False
    if (image_row['hard_banned'] == True):# Do not save hardbanned images.
        return False
    if (image_row['refetch_needed'] == True):# Save images tagged for resaveing.
        return True
    if (image_row['filename_full'] == None):# Image was not saved to start with
        return True
    return False


def save_post_media(db_ses, req_ses, media_base_path, board_name, post):
    """Save media from a post, adding it to the DB.
    Expects py8chan type Post object.
    Commits changes."""
    if (not config.media_enable_saving):
        # If media saving disabled completely
        return
    # Save any new media (from new posts).
    for image in post.all_files():# For each image, if any:
        # Lookup image hash in DB.
        image_find_query = session.query(Image)\
            .filter(Image.hash_md5 == image.file_md5_hex)
        existing_image_row = image_find_query.first()
        if existing_image_row:
            # Check if image needs (re)downloading
            do_redownload = decide_if_media_redownload(
                media_base_path=media_base_path,
                board_name=board_name,
                image_row=image_row
            )
            if (not do_redownload):
                return None# Be fucking explicit about what we're doing.
        # If image not in DB, download image then add it to DB.
        if (config.media_download_enable_full):# If disabled fullsized media files will not be downloaded.
            # Download image:
            # Generate path to save image to
            image_filename = image.filename
            assert2( (type(image_filename) is str), value=image_filename)# Should be text. (Sanity check remote value)
            assert2( (8 <= len(image_filename) <= 128), value=image_filename)# is image hash so about 64 chars. (Sanity check remote value)
            board_path = os.path.join(media_base_path, board_name)
            image_filepath = generate_media_filepath(
                media_base_path=media_base_path,
                media_type='image',# TODO: Validate that 'image' is what we're using for this value
                filename=image.filename
            )
            file_extension = image.file_extension
            assert2( (type(file_extension) is str), value=file_extension)# Should be text. (Sanity check remote value)
            assert2( (0 <= len(file_extension) <= 16), value=file_extension)# Short text. (Sanity check remote value)
            image_url = image.file_url
            assert2( (type(image_url) is str), image_url)# Should be text. (Sanity check remote value)
            assert2( (16 <= len(image_url) <= 256), image_url)# Short text. (Sanity check remote value)
            # Load image from server
            try:
                logging.debug('save_post_media() image_url={0!r}; image_filepath={1!r};'.format(image_url, image_filepath))
                image_resp = common.fetch(
                    requests_session=req_ses,
                    url = image_url,
                )
            except common.FetchGot404 as err:
                logging.exception(err)
                logging.warning('Could not fetch primary remote file, skipping this image.')
                continue# Skip handling of this image download.
            # Save image file
            common.write_file(
                file_path=image_filepath,
                data=image_resp.content
            )
            # Calculate hashes. (We use more than one because hash collisions are a thing.)
            with open(image_filepath, 'rb') as image_f:
                # https://www.pythoncentral.io/hashing-files-with-python/
                # Filesize in bytes
                size_bytes = os.path.getsize(image_filepath)# https://stackoverflow.com/questions/2104080/how-to-check-file-size-in-python
                hash_md5 = common.hash_file_md5(filepath=image_filepath)
                hash_sha1 = common.hash_file_sha1(filepath=image_filepath)
                hash_sha256 = common.hash_file_sha256(filepath=image_filepath)
                hash_sha512 = common.hash_file_sha512(filepath=image_filepath)

            print('BREAKPOINT before md5 check')
            # Sanitycheck recieved file's MD5 against what the server told us. (Do we really need to do this? Does having this check make us less reliable?)
            md5_algorithm_works = (hash_md5 == image.file_md5)
            if (not md5_algorithm_works):
                logging.warning('MD5 IMPLIMENTATION IN USE IS NOT CONSISTENT WITH EXPECTED DATA! DO NOT USE IN PRODUCTION!')# TODO: Crash on this happening once everything else is working.
                logging.debug('hash_md5={0!r}'.format(hash_md5))
                logging.debug('image.file_md5={0!r}'.format(image.file_md5))
                logging.debug('image.file_md5_hex={0!r}'.format(image.file_md5_hex))
                print('BREAKPOINT in md5 check')
            print('BREAKPOINT after md5 check')
        else:
            # If image download disabled:
            # NULL values for unfetched data
            filename_full = None
            size_bytes = None
            hash_md5 = None
            hash_sha1 = None
            hash_sha256 = None
            hash_sha512 = None

        if (config.media_download_enable_thumb):# If disabled thumbnails will not be downloaded.
            # Download thumbnail:
            thumbnail_url = image.thumbnail_url
            # Genreate thumbnail path
            filename_thumbnail = os.path.basename(thumbnail_url)# TODO: Less shitty handling of this. (Feels wrong to use filsystem code for a URL)
            thumbnail_filepath = generate_media_filepath(
                media_base_path=media_base_path,
                media_type='thumb',
                filename=filename_thumbnail
            )
            try:
                # Load thumbnail from server
                thumbnail_resp = common.fetch(
                    requests_session=req_ses,
                    url = thumbnail_url,
                )
            except common.FetchGot404 as err:
                logging.exception(err)
                logging.warning('Could not fetch thumbnail remote file, skipping this image.')# TODO: Decide if missing thumbnail should or should not be enough to skip image add.
                continue# Skip handling of this image download.
            # Save thumbnail file
            common.write_file(
                file_path=thumbnail_filepath,
                data=image_resp.content
            )
        else:
            # If no thumbnail download:
            # NULL values for unfetched data
            filename_thumbnail = None
        # Create DB record for image
        new_image_row = Image(
            # Identification of image characteristics
            size_bytes = size_bytes, # Size of the fullsized image in bytes.
            hash_md5 = hash_md5, # MD5 hash of full file.
            hash_sha1 = hash_sha1, # SHA1 hash of full file.
            hash_sha256 = hash_sha256, # SHA256 hash of full file.
            hash_sha512 = hash_sha512, # SHA512 hash of full file.
            # Files on disk
            file_extension = file_extension, # File extention of the fullview file.
            filename_full = image_filename, # Fullsized media file's filename.
            filename_thumbnail = filename_thumbnail, # Thumbnail's filename. Does not care if OP or reply.
        )
        # Stage new image entry to DB.
        db_ses.add(new_image_row)
        # Commit new image entry.
        db_ses.commit()
        logging.info('Added image to DB: {0!r}'.format(new_image_row))
        time.sleep(config.media_download_interval)# Ratelimiting
        continue# Done saving this image.
    return None# Can we return a list of DB IDs for the media?


def list_db_row_post_ids(thread_row):# UNUSED, REMOVEME?
    """Takes posts field from Dd. Returns unsorted list of post numbers"""
    orig_posts = thread_row.posts
    posts = list(orig_posts)
    post_nums_set = set()# Sets are good for membership checking.
    for post in posts:
        post_num = post['id']
        if (post_num not in post_nums_set):
            post_nums_set.add(post_num)

    post_nums_list = list(post_nums_set)# Convert to list for convenience.
    return post_nums_list


def update_thread( db_ses, req_ses, thread, media_base_path, board_name,):
    """Insert new post information to a thread's entry in the DB.
    If the thread is not already in the DB, add it."""
    logging.debug('update_thread() thread={0!r}'.format(thread))
    print('BREAKPOINT')

    # Load DB row for thread. (or at least try to.)
    thread_find_query = session.query(Thread)\
    .filter(Thread.thread_num == thread.id)
    thread_row = thread_find_query.first()

    if (thread_row):
        # Grab the existing thread data
        logging.debug('thread_row.posts={0!r}'.format(thread_row.posts))
        working_local_posts = list(thread_row.posts)# <-- IMPORTANT!
    else:
        # Thread is new and needs a row created.
        logging.info('Creating row for new thread: {0!r}'.format(thread.id))
        thread_row = Thread(# Create a new thread row for this thread.
            # Addressing
            thread_num = thread.id,
            # Thread data
            posts = None, # JSON encoded posts for this thread
            first_post_num = thread.id, # OP's post num
            last_post_num = thread.last_reply_id, # Most recent reply's post num
            first_seen = datetime.datetime.utcnow()# TODO Check date handling RE timezones
        )
        db_ses.add(thread_row)# Stage new thread row into DB.
        working_local_posts = None

    if working_local_posts is None:# Initialize as empty list if None / NULL
        working_local_posts = []

    logging.debug('working_local_posts={0!r}'.format(working_local_posts))
    # After this point the only interaction with the DB copy of the posts should be immediately before committing thread changes.
    # This is to permit committing image creation without committing changes to posts. <-- IMPORTANT!

    # Isolate new posts
    # (Turn thread object into set of post nums)
    remote_post_nums = set()# A set will handle uniquification/deduplication of nums for us.
    for remote_post in thread.posts:
        remote_post_nums.add(remote_post.num)
    # Get post nums from DB version of thread
    # (Turn DB store of thread into set of post nums)
    db_post_nums = set()# A set will handle uniquification/deduplication of nums for us.
    for db_post in working_local_posts:
        db_post_nums.add(db_post['no'])# I _DO NOT_ like having differing variable names for the same value. TODO: Fix this.

    # Get just posts that are new
    # Should give a new set composed of elements in remote_post nums that are not in db_post_nums without modifying either compared set.
    new_post_nums = remote_post_nums.difference(db_post_nums)# "Return a new set with elements in the set that are not in the others." - https://docs.python.org/3.7/library/stdtypes.html#set-types-set-frozenset

    # Process NEW posts
    for post in thread.posts:# Addressing posts by num?
        post_num = post.num
        logging.debug('update_thread() currently testing post_num={0!r}'.format(post_num))
        if post_num in db_post_nums:
            continue# Post already saved
        save_post_media(
            db_ses=db_ses,
            req_ses=req_ses,
            media_base_path=media_base_path,
            board_name=board_name,
            post=post
        )
        # Add post to thread DB column (only commit after all posts processed)
        # TODO WRITEME
        working_local_posts.append(post._data)# Is there a better way of doing this?

    # Change the DB row.
    thread_row.posts = working_local_posts
    thread_row.first_post_num = thread.id# OP's post num
    thread_row.last_post_num = thread.last_reply_id# Most recent reply's post num
    logging.debug('Committing new version of thread to DB')
    session.commit()
    logging.debug('Finished updating thread {0!r}'.format(thread.id))
    return None# Be fucking explicit about what we're doing.


def mark_thread_dead(db_ses, thread_num):
    logging.debug('Marking thread as dead: {0!r}'.format(thread_num))
    # Load DB row for thread. (or at least try to.)
    thread_find_query = session.query(Thread)\
    .filter(Thread.thread_num == thread_num)
    thread_row = thread_find_query.first()
    if (thread_row):
        # Update for the last time
        thread_row.dead_timestamp = datetime.datetime.utcnow()# FUCKING TIMEZONES. TODO: Consitency check time values.
        thread_row.dead = True
        session.commit()
        logging.debug('Successfully marked thread as dead: {0!r}'.format(thread_num))
    else:
        logging.error('Could not find thread to mark it as dead: {0!r}'.format(thread_num))
    return


def find_db_alive_thread_nums(db_ses, max_results=5000):
    db_alive_thread_nums = set()# Set allows easy difference checking
    alive_find_query = session.query(Thread)\
        .filter(Thread.thread_num == thread_num)\
        [0:max_results]# LIMIT max_results
    for alive_thread_row in alive_find_query:
        db_alive_thread_nums.add(alive_thread_row.thread_num)
    return db_alive_thread_nums


def prune_deleted_threads(db_ses, alive_threads, max_results=5000):
    logging.debug('Pruning dead threads')
    # Grab not-dead threads from DB
    db_alive_thread_nums = set()
    alive_find_query = session.query(Thread)\
        .filter(Thread.dead == True)\
        [0:max_results]# LIMIT max_results
    for alive_thread_row in alive_find_query:
        db_alive_thread_nums.add(alive_thread_row.thread_num)

    # Grab alive threads from latest board update
    board_alive_thread_nums = set()
    for alive_thread in alive_threads:
        board_alive_thread_nums.add(alive_thread.id)

    # Get threads marked alive in DB but not on board
    dead_thread_nums = db_alive_thread_nums.difference(board_alive_thread_nums)
    logging.info('Found {0} dead threads'.format(len(dead_thread_nums)))

    # Mark dead threads as dead
    for dead_thread_num in dead_thread_nums:
        mark_thread_dead(db_ses, dead_thread_num)
    logging.debug('Finished pruning dead threads')
    return

def board_update_loop(db_ses, req_ses, media_base_path, board_name, maximum_dead_threads):
    """Main update loop for one board."""
    loop_counter = 0
    while (True):
        loop_counter += 1
        logging.info('Thread check loop iteration {0}'.format(loop_counter))
        if loop_counter > 200:
            logging.warning('DEBUG EXIT TRIGGERED. Maximum cycles reached.')
            raise DeliberateDevelopmentFuckup()# Throw a crowbar into the cogs so it doesn't run over pedestrians.
        # TODO: Logic to prevent overfilling of threads cache
        logging.debug('Starting to update threads')
        # Update from remote server
        board = py8chan.Board(board_name=board_name)
        threads = board.get_all_threads()# Threads list
        # Notice dead threads and mark them as dead.
        prune_deleted_threads(
            db_ses=db_ses,
            alive_threads=threads,
            max_results=maximum_dead_threads
        )
        # Check each thread that was listed against what we have.
        # - If new.latest_post > local.latest_post: reprocess thread. Otherwise thread is unchanged.
        for thread in threads:
            do_thread_update = False# Should this thread be updated this cycle?
            # Is thread updated?
            thread_number = thread.id
            try:
                dummy = local_threads_update_cache[thread_number]# Ensure thread is in cache
            except KeyError:
                # Thread is new
                # Initialize local version
                local_threads_update_cache[thread_number] = {'last_post_id':0}# Zero because it'll always be less than any post_num.
                # Update thread
                do_thread_update = True
            if (len(thread.replies) != 0):# Only check last post numbers if there is at least one reply
                # Compare the last post of each version of the thread against each other
                if (thread.replies[-1].post_id != local_threads_update_cache[thread_number]['last_post_id']):
                    logging.debug('New post detected in thread')
                    do_thread_update = True
            if do_thread_update:
                # Updated threads need updating.
                # Store new version of thread.
                logging.debug('Updating thread {0}'.format(thread.num))
                update_thread(
                    db_ses=db_ses,
                    req_ses=req_ses,
                    thread=thread,
                    media_base_path=media_base_path,
                    board_name=board_name,
                )
                # Update local updatecheck cache
                local_threads_update_cache[thread_number] = {
                    'last_post_id': thread.replies[-1].post_id
                }
                logging.debug('Finished updating thread {0}'.format(thread.num))
        logging.debug('Finished updating threads')
        time.sleep(config.minimum_board_reload_interval)# Ratelimiting
        continue
    logging.info('Board update loop is somehow returning!')# This line should not ever execute.



# ===== ===== ===== =====
# Warn about dumb settings
if (not config.media_enable_saving):
    logging.warning('Media saving disabled completely! config.media_enable_saving={0!r}'.format(media_enable_saving))
if (not config.media_download_enable_full):
    logging.warning('Media fullsize saving disabled! config.media_download_enable_full={0!r}'.format(media_download_enable_full))
if (not config.media_download_enable_thumb):
    logging.warning('Media thumbnail saving disabled! config.media_download_enable_thumb={0!r}'.format(media_download_enable_thumb))



# ===== ===== ===== =====
# Define DB
# Startup ORM mapping base thingy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def get_threads_table(base, board_name):
    """Dynamically generate the table definition class to permit multiple target boards.
    base should be instance of sqlalchemy.declarative_base()
    returns a sqlalchemy table class.
    """
    table_name = '{0}_threads'.format(board_name)
    class Thread(base):
        """This table is for any and all posts for this board"""
        __tablename__ = table_name
        pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just a primary key.
        # Addressing
        thread_num = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)
        # Thread data
        posts = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)# JSON encoded posts for this thread
        first_post_num = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)# OP's post num
        last_post_num = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)# Most recent reply's post num
        dead = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)# Has this thread been removed from the originating board? (Set TRUE if FALSE but not in catalogue. Only check if alive if currently FALSE)
        dead_timestamp = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=None)# First time the thread was in the DB but not on the board.
        first_seen = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=None)#First time thread was seen on the board by FutaWilly.
        #last_seen = sqlalchemy.column(sqlalchemy.DateTime, nullable=True, default=None)#Last time thread was seen on the board by FutaWilly. (Commented out because it feels like it'd be a resource hog.)TODO: Consider this value's merits.
        # Administrative / legal compliance
        removed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Users can't access thread
        banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Fetcher can't save thread
    return Thread# The newly-defined class


def get_images_table(base, board_name):
    """Dynamically generate the table definition class to permit multiple target boards.
    base should be instance of sqlalchemy.declarative_base()
    returns a sqlalchemy table class.
    """
    table_name = '{0}_images'.format(board_name)
    class Image(base):
        """This table is for any and all images/media associated with posts for this board"""
        __tablename__ = table_name
        # Addressing
        image_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just a primary key. (I don't trust primary keys to work in the long-term. DBs need migrations, merges, ect sometimes.)
        # Identification of image characteristics
        size_bytes = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)# Size of the fullsized image in bytes #TODO!
        hash_md5 = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# MD5 hash of full file #TODO!
        hash_sha1 = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# SHA1 hash of full file #TODO!
        hash_sha256 = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# SHA256 hash of full file #TODO!
        hash_sha512 = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# SHA512 hash of full file #TODO!
        # Files on disk
        file_extension = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# File extention of the fullview file.
        filename_full = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Fullsized media file
        filename_thumb_reply = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Thumbnail used in OP post (if applicable)
        filename_thumb_op = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Thumbnail used in reply post (if applicable)
        filename_thumbnail = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Thumbnail's filename. Does not care if OP or reply.
        # Administrative / legal compliance
        removed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Users can't access file. #TODO!
        banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Fetcher can't save file
        hard_banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Ultra-paranoid ban. Purge from cache, overwrite disk location, recheck for existance on a cronjob, the works. All that remains should be admin logs and hashes used to prevent image ever existing again. Use VERY sparingly. #TODO!
        refetch_needed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Resave the file if it is ever seen again. (For broken media)
        # Hacks (Like running this shit on more than one machine per single instance. Weird use cases and such.)
        # None yet.
    return Image# The newly-defined class


# Build classes. (Table definitions)
# This needs to be done once per board, each time we start the program.
# TODO: Move this to be closer/more local to fetcher
Thread = get_threads_table(base=Base, board_name='v')
Image = get_images_table(base=Base, board_name='v')


# ===== ===== ===== =====
# Spinup DB
logging.info('Starting DB connection...')

# DB Configuration
db_filepath = config.db_filepath
db_connection_string = config.db_connection_string

# SQLite3
# Ensure DB path is available
if (db_filepath):# Don't bother if no filepath given.
    db_dir = os.path.dirname(db_filepath)
    logging.debug('db_dir = {0!r}'.format(db_dir))
    if db_dir:# Only try to create dir if a dir is given.
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
db_ses = session# TEMPORARY! TODO: Move shit into functions so we can remove this
logging.info('DB connection established.')


# ===== ===== ===== =====
# Setup requests session
req_ses = requests.session()

# ===== ===== ===== =====
# Cache of local threads
# Initialize state
local_threads_update_cache = {}# THREAD_NUM: LAST_POST_NUM

# ===== ===== ===== =====
# Start looping over remote threads
board_update_loop(
    db_ses=db_ses,
    req_ses=req_ses,
    media_base_path=config.media_base_path,
    board_name=config.board_name,
    maximum_dead_threads=config.maximum_dead_threads,
)

# ===== ===== ===== =====
# Host the DB threads as a webapp
# TODO


# ===== ===== ===== =====
logging.info('EOF')# End of file