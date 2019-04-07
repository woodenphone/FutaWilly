#-------------------------------------------------------------------------------
# Name:        database.py
# Purpose: Futawilly Databse code.
#
# Author:      Ctrl-S
#
# Created:     05-04-2019
# Copyright:   (c) Ctrl-S 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Imports
# stdlib
import logging
# Remote libraries
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
# Local modules

# Startup ORM mapping base thingy
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
        # Databse Meta-Recordkeeping. (Creations, updates, etc)
        # row_created = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=?)# TODO: FIGURE OUT CODE FOR THIS.
        # row_modified = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=?)# TODO: FIGURE OUT CODE FOR THIS.
    return Image# The newly-defined class



def get_images_todo_table(base, board_name):# WIP; NOT YET IMPLIMENTED!
    """Dynamically generate the table definition class to permit multiple target boards.
    base should be instance of sqlalchemy.declarative_base()
    returns a sqlalchemy table class.
    """
    table_name = '{0}_todo_images'.format(board_name)
    class TodoImage(base):
        """This table is for images that need downloading.
        The data in this table IS NOT persistant over time.
        This table is purely for download queueing.
        Any row with in_progress over 24Hrs ago should have it's inprogress info reset on the assumption that it is broken.
        """
        __tablename__ = table_name
        # Addressing
        image_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)# Just a primary key. (I don't trust primary keys to work in the long-term. DBs need migrations, merges, ect sometimes.)
        # Todo-list meta
        timestamp_todo_created# When this row was created, for pruning old entries.
        timestamp_todo_exipre# When should this row be considered 'too old' and discarded wiwthout use?, for pruning old entries. (Should probably be less than a month in the future.)
        # Any row with in_progress over 24Hrs ago should have it's inprogress info reset on the assumption that it is broken.
        in_progress_timestamp# Timestamp of attempt start if being downloaded, otherwise NULL for not yet started.
        in_progress# Is a download thread working on this? TRUE if being used, FALSE if not being used, NULL if we don't know what's happening.
        # Origin info. (Probably pointless to include.)
        origin_post_num# Post number that triggered this item to be added to this table.
        origin_thread_num# Thread containing post that added this entry.
        origin_boardname# What is the shortname of the origin board?
        expected_hash_md5# The MD5 hash we were told by the post(Is this worth having?)
        # Remote location. (The most important part of this table)
        url_full_view# Fullsize.
        url_thumb_reply# Reply thumbnail.
        url_thumb_op# OP thumbnail.
        # Files on disk.
        file_extension = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# File extention of the fullview file.
        filename_full = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Fullsized media file
        filename_thumb_reply = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Thumbnail used in OP post (if applicable)
        filename_thumb_op = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Thumbnail used in reply post (if applicable)
        filename_thumbnail = sqlalchemy.Column(sqlalchemy.Unicode, nullable=True)# Thumbnail's filename. Does not care if OP or reply.
        # Databse Meta-Recordkeeping. (Creations, updates, etc)
        # row_created = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=?)# TODO: FIGURE OUT CODE FOR THIS.
        # row_modified = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=?)# TODO: FIGURE OUT CODE FOR THIS.
    return TodoImage# The newly-defined class



def main():
    pass

if __name__ == '__main__':
    main()
