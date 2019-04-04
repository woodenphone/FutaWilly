#! /usr/bin/python3
# Expects python 3.x
#-------------------------------------------------------------------------------
# Name:        py8chan_converters.py
# Purpose: Convert py8chan types into more-easily serealizable python base types
#           or JSON strings
# Author:      Ctrl-S
#
# Created:     04-04-2019
# Copyright:   (c) Ctrl-S 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Imports
# stdlib
import json
# Remote libraries
import py8chan
# Local modules
from fuckups import *# Local Exceptions







# =====
# Conversion functions from py8chan -> json strings.
##def convert_thread_to_json(py8chan_thread):
##    thread_dict = convert_thread_to_dict(py8chan_thread)
##    thread_json = json.dumps(post_dict)
##    return thread_json


def convert_post_to_json(py8chan_post):
    post_dict = convert_post_to_dict(py8chan_post)
    post_json = json.dumps(post_dict)
    return post_json


def convert_file_to_json(py8chan_file):
    file_dict = convert_post_to_dict(py8chan_post)
    file_json = json.dumps(post_dict)
    return file_json


# =====
# Conversion functions from py8chan -> python base types.
def convert_thread_to_dict(py8chan_thread):
    """Turn py8chan Thread into a dict of only native python object types.
    See py8chan thread.py"""
    assert(type(py8chan_thread) is py8chan.Thread)# Expects py8chan.Thread object.

    files = []
    for thread_file in py8chan_thread.files:# "file" is a keyword, so avoid using it as a variable name.
        file_dict = convert_file_to_dict(thread_file)
        files.append(file_dict)

    all_posts = []
    for thread_post in py8chan_thread.all_posts:
        post_dict = convert_post_to_dict(thread_post)
        all_posts.append(post_dict)

    thread_dict = {# TODO: All values for a thread
        'id': py8chan_thread.id,
        '_api_url': py8chan_thread._api_url,
        'closed': py8chan_thread.closed,
        'sticky': py8chan_thread.sticky,
        '_last_modified': py8chan_thread._last_modified,
        'files': files,
        'url': py8chan_thread.url,
        'all_posts': all_posts,
        'TODO': py8chan_thread.TODO,
        'TODO': py8chan_thread.TODO,
        'TODO': py8chan_thread.TODO,
    }
    raise UnimplimentedFuckUp()# Still have not figured out how to handle some of this stuff.
    return thread_dict


def convert_post_to_dict(py8chan_post):
    """Turn py8chan Post into a dict of only native python object types.
    See py8chan thread.py"""
    assert(type(py8chan_post) is py8chan.Post)# Expects py8chan.Post object.
    first_file = None
    all_files = []
    extra_files = []
    c = 0
    for post_file in py8chan_post.all_files:
        c += 1
        post_file_dict = convert_file_to_dict(post_file)
        all_files.append(post_file_dict)
        if c == 1:
            first_file = post_file_dict
        else:
            extra_files.append(post_file_dict)

    post_dict = {
        'post_id': py8chan_post.post_id,
        'poster_id': py8chan_post.poster_id,
        'name': py8chan_post.name,
        'email': py8chan_post.email,
        'tripcode': py8chan_post.tripcode,
        'subject': py8chan_post.subject,
        'comment': py8chan_post.comment,
        'html_comment': py8chan_post.html_comment,# This WILL recieve malicious input.
        'text_comment': py8chan_post.text_comment,# This WILL recieve malicious input.
        'is_op': py8chan_post.is_op,
        'timestamp': py8chan_post.timestamp,
        'datetime': py8chan_post.datetime,
        'first_file': first_file,# This will not work because there are subobjects
        'all_files': all_files,# This will not work because there are subobjects
        'extra_files': extra_files,# This will not work because there are subobjects
        'has_file': py8chan_post.has_file,
        'has_extra_files': py8chan_post.has_extra_files,
        'url': py8chan_post.url,
    }
    return post_dict


def convert_file_to_dict(py8chan_file):
    """Turn py8chan File into a dict of only native python object types.
    See py8chan thread.py"""
    assert(type(py8chan_file) is py8chan.File)# Expects py8chan.File object.
    file_dict = {
        'file_md5': py8chan_file.file_md5,
        'file_md5_hex': py8chan_file.file_md5_hex,
        'filename_original': py8chan_file.filename_original,
        'filename': py8chan_file.filename,
        'file_url': py8chan_file.file_url,
        'file_extension': py8chan_file.file_extension,
        'file_size': py8chan_file.file_size,
        'file_width': py8chan_file.file_width,
        'file_height': py8chan_file.file_height,
        'thumbnail_width': py8chan_file.thumbnail_width,
        'thumbnail_height': py8chan_file.thumbnail_height,
        'thumbnail_fname': py8chan_file.thumbnail_fname,
        'thumbnail_url': py8chan_file.thumbnail_url,
    }
    return file_dict












def main():
    pass# Slack off.

if __name__ == '__main__':
    main()# Don't even bother to set up module-level logger for debugging. MAXIMUM LAZY.
