#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Ctrl-S
#
# Created:     22-04-2019
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
import time
# Remote libraries
#import flask
import sqlalchemy
import py8chan
import requests
import eventlet
# Local modules
import common
import config.futawilly_config as config
from fuckups import *# Local Exceptions
from database import get_threads_table, get_images_table, Base
import config.audit as audit_cfg

# TODO: Audit trails/logs
# TODO: Reasons
# TODO: Takedown transparency log page



# ===== ===== ===== =====
# Normal removal functions for normal janitors/mods.
def ban_file(db_ses, mod_creds, file_md5, reason):
    """Remove all instances of the file from this board...
    and prevent it from reappearing until it is un-removed by another mod action.
    """
    logging.info('Removing file: {hash}'.format(hash=file_md5))
    # Find row
    # Set row to disabled
    logging.info('Successfully removed image: {hash}'.format(hash=file_md5))
    return


def remove_post(db_ses, mod_creds, board, post_num, reason):
    """Remove the specified post from the specified board.

    """
    logging.info('Removing post: {board}.{hash}'.format(board=board, hash=file_md5))
    # Find row
    # Set row to disabled
    logging.info('Successfully removed post: b.{board}-n.{post_num}'.format(board=board, hash=file_md5))
    return


def remove_image(db_ses, mod_creds, board, thread_num, post_num, reason):
    """Remove one image from one post

    """
    logging.info('Removing post: {board}.{hash}'.format(board=board, hash=file_md5))
    # Find row
    # Set row to disabled
    logging.info('Successfully removed post: b.{board}-n.{post_num}'.format(board=board, hash=file_md5))
    return


def remove_thread(db_ses, mod_creds, board, thread_num, reason):
    """Remove the specified thread.

    """
    logging.warning('Moderator:{mod!r} is changing the DB!'.format(mod=mod_creds))# Shitty logfile audit trail
    logging.info('Removing post: {board}.{hash}'.format(board=board, hash=file_md5))
    # Find row
    # Set row to disabled
    logging.info('Successfully removed post: {board}.{hash}'.format(board=board, hash=file_md5))
    return


# ===== ===== ===== =====
# Normal removal functions for normal janitors/mods.



# ===== ===== ===== =====
# Ludicrously dangerous removal functions for supermods
# Don't run these unless you know exactly what you are doing and have slept on it.

def hardban_file(db_ses, mod_creds, file_md5, reason):
    """Don't use this if it possible not to.
    Seriously. This will not be recoverable from if you misuse it.
    You will be tarred and feathered."""
    logging.warning('NUKING FILE FROM ORBIT!')
    logging.info('Removing file: {hash}'.format(hash=file_md5))
    # Find file row

    # Secure erase file on disk

    # TODO: Force cache purge

    logging.info('Successfully hardbanned file: {hash}'.format(hash=file_md5))
    return



def main():
    pass

if __name__ == '__main__':
    main()
