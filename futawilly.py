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


def generate_media_filepath(base_path, media_type, filename):
    a = filename[0:1]
    b = filename[1:4]
    filepath = os.path.join(base_path, media_type, a, b, filename)
    return filepath


def save_media_file(req_ses, base_path, media_type, url, filename):
    """Save a file to the media dir."""
    filepath = generate_media_filepath(base_path=base_path, media_type=media_type, filename=filename)
    logging.debug('save_media_file() url={0!r}; filename={1!r};'.format(url, filename))
    # Load image from server
    media_resp = common.fetch(
        requests_session=req_ses,
        url = url,
    )
    if (not media_resp):
        logging.error('No media response!')
        raise WeFuckedUp()# TODO: Handle failure to retreive image
    else:
        # Save image file
        common.write_file(
            file_path=filepath,
            data=media_resp.content
        )
    raise UnimplimentedFuckUp()# This is not ready for use!
    return None# Be fucking explicit about what we're doing.


def save_post_media(db_ses, req_ses, base_path, board_name, post):
    """Save media from a post, adding it to the DB.
    Expects py8chan type Post object.
    Commits changes."""
    # Save any new media (from new posts).
    for image in post.all_files():# For each image, if any:
        # Lookup image hash in DB.
        image_find_query = session.query(Image)\
            .filter(Image.hash_md5 == image.file_md5_hex)
        existing_image_row = image_find_query.first()
        if existing_image_row:
            # Nothing needed to be done, we already have the file so all that is needed is a DB association.
            # TODO: Process all images in a thread simultaneously for greater speed maybe?
            #return existing_image_row.image_id# For faster DB lookup on retreival this can be used as a foreign key. (Hashes should be 'canonical' association value though?)
            return None# Be fucking explicit about what we're doing.
        # If image not in DB, download image then add it to DB.
        # Download image
        # Generate path to save image to
        image_filename = image.filename
        assert2( (type(image_filename) is str), value=image_filename)# Should be text. (Sanity check remote value)
        assert2( (8 <= len(image_filename) <= 128), value=image_filename)# is image hash so about 64 chars. (Sanity check remote value)
        board_path = os.path.join(base_path, board_name)
        image_filepath = generate_media_filepath(
            base_path=base_path,
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

        # Download thumbnail
        thumbnail_url = image.thumbnail_url
        # Genreate thumbnail path
        filename_thumbnail = os.path.basename(thumbnail_url)# TODO: Less shitty handling of this. (Feels wrong to use filsystem code for a URL)
        thumbnail_filepath = generate_media_filepath(
            base_path=base_path,
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


def update_thread( db_ses, req_ses, thread, base_path, board_name,):
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
        working_local_posts = list(thread_row.posts)
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
        )
        db_ses.add(thread_row)# Stage new thread row into DB.
        working_local_posts = []

    logging.debug('working_local_posts={0!r}'.format(working_local_posts))
    # After this point the only interaction with the DB copy of the posts should be immediately before committing thread changes.
    # This is to permit committing image creation without committing changes to posts.

    # Isolate new posts
    # (Turn thread object into set of post nums)
    remote_post_nums = set()# A set will handle uniquification/deduplication of nums for us.
    for remote_post in thread.posts:
        remote_post_nums.add(remote_post.num)

    # Get post nums from DB version of thread
    # (Turn DB store of thread into set of post nums)
    db_post_nums = set()# A set will handle uniquification/deduplication of nums for us.
    for db_post in working_local_posts:
        db_post_nums.add(db_post.no)# I _DO NOT_ like having differing variable names for the same value. TODO: Fix this.

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
            base_path=base_path,
            board_name=board_name,
            post=post
        )

        # Add post to thread DB column (only commit after all posts processed)
        # TODO WRITEME
        working_local_posts.append(post._data)# Is there a better way of doing this?

    # Change the DB row.
    thread_row.posts = working_local_posts
    thread_row.first_post_num = thread.id, # OP's post num
    thread_row.last_post_num = thread.last_reply_id, # Most recent reply's post num
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
        .filter(Thread.thread_num == thread_num)\
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
        dead = sqlalchemy.column(sqlalchemy.Boolean, nullable=True, default=False)# Has this thread been removed from the originating board? (Set TRUE if FALSE but not in catalogue. Only check if alive if currently FALSE)
        dead_timestamp = sqlalchemy.column(sqlalchemy.DateTime, nullable=True, default=None)# First time the thread was in the DB but not on the board.
        first_seen = sqlalchemy.column(sqlalchemy.DateTime, nullable=True, default=None)#First time thread was seen on the board by FutaWilly.
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
        banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Fetcher can't save file #TODO!
        hard_banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Ultra-paranoid ban. Purge from cache, overwrite disk location, recheck for existance on a cronjob, the works. Use VERY sparingly. #TODO!
        refetch_needed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=0)# Resave the file if it is ever seen again. (For broken media) #TODO!
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
db_ses = session# TEMPORARY! TODO: Move shit into functions so we can remove this

logging.info('DB connection established.')


# ===== ===== ===== =====
# Cache of local threads
# Initialize state
local_threads = {}




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
# Setup requests session
req_ses = requests.session()



# ===== ===== ===== =====
# Start looping over remote threads
base_path = config.media_base_path
board_name = config.board_name
maximum_dead_threads = config.maximum_dead_threads
loop_counter = 0
while (True):
    loop_counter += 1
    logging.debug('Thread check loop iteration {0}'.format(loop_counter))
    if loop_counter > 2:
        logging.warning('DEBUG EXIT TRIGGERED. 2 cycles finished.')
        raise DeliberateDevelopmentFuckup()# Throw a crowbar into the cogs so it doesn't run over pedestrians.

    # TODO: Logic to prevent overfilling of threads cache

    # Update from remote server
    logging.debug('Starting to update threads')
    # Threads list
    board = py8chan.Board(board_name=board_name)
    threads = board.get_all_threads()
    logging.debug('threads={0!r}'.format(threads))
    print('BREAKPOINT')

    # Notice dead threads and mark them as dead.
    prune_deleted_threads(
        db_ses=db_ses,
        alive_threads=threads,
        max_results=5000
    )

    # Check each thread that was listed against what we have.
    # - If new.latest_post > local.latest_post: reprocess thread. Otherwise thread is unchanged.
    for thread in threads:
        logging.debug('thread={0!r}'.format(thread))
        do_thread_update = False# Should this thread be updated this cycle?
        print('BREAKPOINT')
        # Is thread updated?
        # Compare last post number
        thread_number = thread.id
        try:
            current_thread = local_threads[thread_number]
        except KeyError:
            # Thread is new
            # Initialize local version
            local_threads[thread_number] = {}
            # Update thread
            do_thread_update = True

        # Compare the last post of each version of the thread against each other
        if (len(thread.replies) != 0):
            # Only check last post numbers if there is at least one reply
            if (thread.replies[-1].post_id != current_thread.replies[-1].post_id):
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
                thread=thread,
                base_path=base_path,
                board_name=board_name,
            )
            logging.debug('Finished updating thread {0}'.format(thread.num))
##            logging.warning('DEBUG EXIT TRIGGERED. One thread processed.')
##            raise DeliberateDevelopmentFuckup()# Throw a crowbar into the cogs so it doesn't run over pedestrians.

    logging.debug('Finished updating threads')
    continue



# ===== ===== ===== =====
# Host the DB threads as a webapp
# TODO


# ===== ===== ===== =====
logging.info('EOF')# End of file