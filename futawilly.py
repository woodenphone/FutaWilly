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
# Remote libraries
#import flask
import sqlalchemy
import py8chan
import requests
# Local modules
import common
import config.futawilly_config as config



class FuckUp(Exception):
    """
    Local exception superclass.
    Someone fucked up.
    Something went wrong and we need to signal that fact.
    """
    pass# Nothing to do in an exception class like this other than hold a name.


class WeFuckedUp(FuckUp):
    """
    We fucked up.
    Something went wrong with this code.
    Bad coder.
    See RFC 7231 section 6.6 at https://tools.ietf.org/html/rfc7231#section-6.6
    """
    pass# Nothing to do in an exception class like this other than hold a name.



class YouFuckedUp(FuckUp):
    """
    You fucked up.
    Something went wrong that is all the user's fault.
    Bad user.
    See RFC 7231 section 6.5 at https://tools.ietf.org/html/rfc7231#section-6.5
    """
    pass# Nothing to do in an exception class like this other than hold a name.



class TheyFuckedUp(FuckUp):
    """
    The Man fucked up.
    Something went wrong that is neither this code's nor the user's fault.
    Goddamnit.
    """
    pass# Nothing to do in an exception class like this other than hold a name.



class AssertAFuckupHappened(FuckUp, AssertionError):
    """
    Something got fucked up and we noticed.
    This is basically an Assertion replacement.
    """
    pass# Nothing to do in an exception class like this other than hold a name.




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

def assert2(exp, value=None, msg=None):
    """Custom Assert function.
    exp: Assert fires if not True.
    value: Value that is being tested, logged via logging when assert fires.
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
        logging.error('ASSERT2 FIRED WITH VALUE: {0!r}'.format(value))
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
        reuests_session=req_ses,
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
    assert(False)# This is not ready for use!
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
        assert2( (type(image_filename) is unicode), value=image_filename)# Should be text. (Sanity check remote value)
        assert2( (8 <= len(image_filename) <= 64), value=image_filename)# is image hash so about 32 chars. (Sanity check remote value)
        board_path = os.path.join(base_path, board_name)
        image_filepath = generate_media_filepath(
            base_path=base_path,
            media_type='image',# TODO: Validate that 'image' is what we're using for this value
            filename=image.filename
        )
        file_extention = image.file_extention
        assert2( (type(file_extention) is unicode), value=file_extention)# Should be text. (Sanity check remote value)
        assert2( (0 <= len(file_extention) <= 8), value=file_extention)# Short text. (Sanity check remote value)
        image_url = image.file_url
        assert2( (type(image_url) is unicode), value=image_url)# Should be text. (Sanity check remote value)
        assert2( (16 <= len(image_url) <= 256), value=image_url)# Short text. (Sanity check remote value)
        # Load image from server
        logging.debug('save_post_media() image_url={0!r}; image_filepath={1!r};'.format(image_url, image_filepath))
        image_resp = common.fetch(
            reuests_session=req_ses,
            url = image_url,
        )
        if (not image_resp):
            logging.error('No image response!')
            raise WeFuckedUp()# TODO: Handle failure to retreive image
        else:
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
                # MD5 hash
                hash_md5 = common.hash_file_md5(filepath=image_filepath)
                # Sanitycheck recieved file's MD5 against what the server told us
                # SHA1 hash
                hash_sha1 = common.hash_file_sha1(filepath=image_filepath)
                # SHA256 hash
                hash_sha256 = common.hash_file_sha256(filepath=image_filepath)
                # SHA1 hash
                hash_sha512 = common.hash_file_sha512(filepath=image_filepath)

        # Download thumbnail
        # Genreate thumbnail path
        filename_thumbnail = os.path.basename(thumbnail_url)# TODO: Less shitty handling of this. (Feels wrong to use filsystem code for a URL)
        thumbnail_filepath = generate_media_filepath(
            base_path=base_path,
            media_type='thumb',
            filename=filename_thumbnail
        )
        # Load thumbnail from server
        thumbnail_resp = common.fetch(
            reuests_session=req_ses,
            url = image.thumbnail_url,
        )
        if (not thumbnail_resp):
            logging.error('No thumbnail response!')
            raise WeFuckedUp()# TODO: Handle failure to retreive thumbnail
        else:
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
            file_extention = file_extention, # File extention of the fullview file.
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


def list_db_row_post_ids(posts):
    """Takes posts field from Dd. Returns unsorted list of post numbers"""
    post_nums = []
    for post in posts:
        if post['post']:# TODO FIX THIS; TODO WRITEME
            pass# TODO FIX THIS; TODO WRITEME
        pass# TODO FIX THIS; TODO WRITEME
    pass# TODO FIX THIS; TODO WRITEME
    assert(False)# This is not ready for use!
    return post_ids


def update_thread( db_ses, req_ses, thread, base_path, board_name,):
    """Insert new post information to a thread's entry in the DB.
    If the thread is not already in the DB, add it."""
    logging.debug('update_thread() thread={0!r}'.format(thread))
    print('BREAKPOINT')
    thread_num = thread.id
    assert2( (type(thread_num) is int), value=thread_num)

    # Load DB row for thread. (or at least try to.)
    thread_find_query = session.query(Thread)\
    .filter(Thread.thread_num == thread_num)
    thread_row = thread_find_query.first()

    if (thread_row):
        # Grab the existing thread data
        logging.debug('thread_row.posts={0!r}'.format(thread_row.posts))
        working_local_posts = list(thread_row.posts)
    else:
        # Thread is new and needs a row created.
        logging.info('Creating row for new thread: {0!r}'.format(thread_num))
        # TODO WRITEME!
        thread_row = Thread()# Will this line work?
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
        db_post_nums.add(db_post.num)

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
        assert(False)# TODO
        working_local_posts.append(post._data)# HACK AND SHOULD BE CHANGED! TODO: IMPROVE THIS

    # Change the DB row.
    # TODO CODEME
    thread_row.posts = working_local_posts


    logging.debug('Committing new version of thread to DB')
    session.commit()
    logging.debug('Finished updating thread {0!r}'.format(thread_num))
    return None# Be fucking explicit about what we're doing.





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
    pk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just a primary key. (I don't trust primary keys to work in the long-term. DBs need migrations, merges, ect sometimes.)
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
    filename_thumbnail = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Thumbnail's filename. Does not care if OP or reply.
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
db_ses = session# TEMPORARY! TODO: Move shit into functions so we can remove this

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
# Setup requests session
req_ses = requests.session()



# ===== ===== ===== =====
# Start looping over remote threads
base_path = config.media_base_path
board_name = config.board_name
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
    logging.debug('threads={0!r}'.format(threads))
    print('BREAKPOINT')

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

    logging.debug('Finished updating threads')
    continue



# ===== ===== ===== =====
logging.info('EOF')# End of file