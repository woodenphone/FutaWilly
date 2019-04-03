#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     04-09-2018
# Copyright:   (c) User 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# StdLib
import time
import os
import random
import argparse
import sys
import logging
import logging.handlers
import datetime
import re
import hashlib
# Remote libraries
import requests
import requests.exceptions


# ===== ===== =====
# Logging setup
def setup_logging(log_file_path,timestamp_filename=True,max_log_size=104857600):
    """Setup logging (Before running any other code)
    http://inventwithpython.com/blog/2012/04/06/stop-using-print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
    """
    assert( len(log_file_path) > 1 )
    assert( type(log_file_path) == type("") )
    global logger

    # Make sure output dir(s) exists
    log_file_folder =  os.path.dirname(log_file_path)
    if log_file_folder is not None:
        if not os.path.exists(log_file_folder):
            os.makedirs(log_file_folder)

    # Add timetamp for filename if needed
    if timestamp_filename:
        # http://stackoverflow.com/questions/8472413/add-utc-time-to-filename-python
        # '2015-06-30-13.44.15'
        timestamp_string = datetime.datetime.utcnow().strftime("%Y-%m-%d %H.%M.%S%Z")
        # Full log
        log_file_path = add_timestamp_to_log_filename(log_file_path,timestamp_string)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # TODO: Put new log message format example here
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - f.%(filename)s - ln.%(lineno)d - %(message)s")

    # File 1, log everything
    # https://docs.python.org/2/library/logging.handlers.html
    # Rollover occurs whenever the current log file is nearly maxBytes in length; if either of maxBytes or backupCount is zero, rollover never occurs.
    fh = logging.handlers.RotatingFileHandler(
        filename=log_file_path,
        # https://en.wikipedia.org/wiki/Binary_prefix
        # 104857600 100MiB
        maxBytes=max_log_size,
        backupCount=10000,# Ten thousand should be enough to crash before we reach it.
        )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console output
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logging.info("Logging started.")
    return logger

def add_timestamp_to_log_filename(log_file_path,timestamp_string):
    """Insert a string before a file extention"""
    base, ext = os.path.splitext(log_file_path)
    return base+"_"+timestamp_string+ext


# ===== ===== ===== =====
# Fetching remote resources

class FetchGot404(Exception):
    def __init__(self, url, response):
        self.url = url
        self.response = response
    """Pass on that there was a 404."""



def fetch(requests_session, url, method='get', data=None, expect_status=200, headers=None, max_attempts=5):
##    logging.debug('fetch() arguments = {0!r}'.format(locals()))# Log function arguments
#    headers = {'user-agent': user_agent}
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
##    user_agent ='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    if headers is None:
        headers = {'user-agent': user_agent}
    elif 'user-agent' not in headers.keys():
        headers['user-agent'] = user_agent

    if headers:
        headers.update(headers)

    for try_num in range(5):
        logging.debug('Fetch {0!r}'.format(url))
        try:
            if method == 'get':
                response = requests_session.get(url, headers=headers, timeout=300)
            elif method == 'post':
                response = requests_session.post(url, headers=headers, data=data, timeout=300)
            else:
                raise Exception('Unknown method')
        except requests.exceptions.Timeout as err:
            logging.exception(err)
            logging.error('Caught requests.exceptions.Timeout')
            continue
        except requests.exceptions.ConnectionError as err:
            logging.exception(err)
            logging.error('Caught requests.exceptions.ConnectionError')
            continue
        # Allow certain error codes to be passed back out
        if response.status_code == 404:
            logging.error("fetch() 404 for url: %s" % url)
            write_file(file_path=os.path.join('debug', 'fetch_last_404.htm'), data=response.content)# Save 404 page for debugging
            raise FetchGot404(url=url,response=response)
        if response.status_code != expect_status:
            logging.error('Problem detected. Status code mismatch. Sleeping. expect_status: %s, response.status_code: %s' % (expect_status, response.status_code))
            write_file(file_path=os.path.join('debug', 'fetch_last_misc_bad_status_code.htm'), data=response.content)# Save page for debugging
            time.sleep(60*try_num)
            continue
        else:
            write_file(file_path=os.path.join('debug', 'fetch_last_success.htm'), data=response.content)# Save page for debugging
            time.sleep(random.uniform(0.5, 3.5))
            return response

    raise Exception('Giving up!')


# ===== ===== ===== =====
# File reading and writing

def write_file(file_path, data):
    """Write to an file.
    Create dir if destination dir does not exist"""
    # Ensure output dir exists
    folder = os.path.dirname(file_path)
    if folder:
        if not os.path.exists(folder):
            os.makedirs(folder)
    assert(os.path.exists(os.path.dirname(file_path)))
    with open(file_path, 'wb') as f:
        f.write(data)
    return


def read_file(file_path):
    """Read from a file. Fail if file does not exist"""
    assert(os.path.exists(file_path))
    with open(file_path, 'rb') as f:
        data = f.read()
    return data


# ===== ===== ===== =====
# Hashing functions
def hash_file_md5(filepath):
    """Generate MD5 hash for a file"""
    #https://www.pythoncentral.io/hashing-files-with-python/
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(filepath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    file_md5 = hasher.hexdigest()
    return file_md5


def hash_file_sha1(filepath):
    """Generate SHA1 hash for a file"""
    # https://www.pythoncentral.io/hashing-files-with-python/
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filepath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    file_sha1 = hasher.hexdigest()
    return file_sha1


def hash_file_sha256(filepath):
    """Generate SHA256 hash for a file"""
    # https://www.pythoncentral.io/hashing-files-with-python/
    BLOCKSIZE = 65536
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    file_sha256 = hasher.hexdigest()
    return file_sha256


def hash_file_sha512(filepath):
    """Generate SHA512 hash for a file"""
    # https://www.pythoncentral.io/hashing-files-with-python/
    BLOCKSIZE = 65536
    hasher = hashlib.sha512()
    with open(filepath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    file_sha512 = hasher.hexdigest()
    return file_sha512


# ===== ===== ===== =====
#


def main():
    pass

if __name__ == '__main__':
    main()
