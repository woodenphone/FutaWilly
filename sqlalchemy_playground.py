#! /usr/bin/python3
# Expects python 3.x
#-------------------------------------------------------------------------------
# Name:        sqlalchemy playground
# Purpose:
#
# Author:      Ctrl-S
#
# Created:     26-03-2019
# Copyright:   (c) Ctrl-S 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# StdLib
import logging
import logging.handlers
import datetime
import os
# Remote libraries
import sqlalchemy# For talking to DBs
from sqlalchemy.ext.declarative import declarative_base
# local
import utils


def main():
    pass

if __name__ == '__main__':
    utils.setup_logging(os.path.join("debug", "sqlalchemy_playground.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception as e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")




# ===== ===== ===== =====
# Define DB
# Startup ORM mapping base thingy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

##from sqlalchemy import Column, Integer, String

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


# SQLite3
# DB Configuration
db_filepath = os.path.join('tmp', 'sql_play.db')# For sqllite
db_connection_string = 'sqlite:///tmp/sql_play.db'

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



# Start the DB engine
engine = sqlalchemy.create_engine(
    db_connection_string,# Points SQLAlchemy at a DB
    echo=True# Output DB commands to log
)
Base.metadata.create_all(engine, checkfirst=True)# Create tables based on classes. (checkfirst only creates if it doesn't exist already)



# ===== ===== ===== =====
# Work with DB

# Create a session to interact with the DB
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()



# Test if a thread is saved
logging.info('Cheacking for thread existence...')
thread_num = 123


thread_check_query = session.query(Thread)\
    .filter(Thread.thread_num == thread_num)
thread_check_result = thread_check_query.first()
if thread_check_result:
    thread_exists = True
else:
    thread_exists = False
logging.info('Thread {0} exists: {1}'.format(thread_num, thread_exists))


if not thread_exists:
    # Insert a thread
    logging.info('Inserting a thread...')
    first_posts = {
        'thread_num': 1,
        'posts': [
            {
            'post_num': 1,
            'comment': 'lorem ipsum',
            },
        ]
    }
    new_thread_row = Thread(thread_num=thread_num, posts=first_posts)
    session.add(new_thread_row)
    session.commit()
    logging.info('Thread inserted.')

# Update a thread
logging.info('Updating a thread...')
second_posts = {
    'thread_num': 1,
    'posts': [
        {
        'post_num': 1,
        'comment': 'lorem ipsum',
        },
        {
        'post_num': 2,
        'comment': 'dol doreum',
        },
    ]
}
update_find_query = session.query(Thread)\
    .filter(Thread.thread_num == thread_num)
row_to_update = update_find_query.first()
if not row_to_update:
    logging.error('Thread not found! {0!r}'.format(thread_num))
row_to_update.posts = second_posts
session.commit()
logging.info('Thread updated.')


# Remove a thread
logging.info('Deleting a thread...')
delete_find_query = session.query(Thread)\
    .filter(Thread.thread_num == thread_num)
row_to_delete = delete_find_query.first()
session.delete(row_to_delete)
session.commit()
logging.info('Thread deleted')





