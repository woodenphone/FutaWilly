#! /usr/bin/python3
# database_playground.py
# Database definistion and playground
#
# =====
# Imports
# stdlib
import os
import logging
# Remote libraries
import sqlalchemy
# Local modules
import common
import config.database_playground_config as config




# ===== ===== ===== =====
# Core data tables

class Thread():
    """Table to represent a single infinitychan thread."""
    thread_num = sqlalchemy# thread_num
    # low_post_num
    # high_post_num
    # posts_json
    # last-seen
    # last_modified
    # last_updated
    # first_seen
    # OP_Timestamp
    pass# TODO



class Board():
    """Table to represent a single infinitychan board."""
    # Shortname
    # Longname
    # Subtitle
    # Default_Username
    # Last_checked
    # check_interval
    pass# TODO



class Image():
    """Table to represent infinitychan images (or other media file).
    The original filenames are stored with the post they occured on."""
    # Filepath
    # Size
    # MD5
    # SHA1
    # SHA512
    # Missing? (If True: Redownload when seen.)
    # Deleted? (If True: Do not serve content.)
    # Banned? (If True: Do not download.)
    # Hard_Banned (If True: Overwrite any occurances of any version of the file, leaving only identification data to further prevent it from existing. Purge from CDNs, ect..)
    pass# TODO



# ===== ===== ===== =====
# Logs and hard-ban support
#
# Single-post removal
class PostDeletion():
    """Table to represent single-post deletion events."""
    pass# TODO



class PostBan():
    """Table to represent single-post bans."""
    pass# TODO
    # Banned-by-username
    # Banned-by-user-id
    # Banned-by-usertype
    # Reason-text
    # reason-tags
    # ban-started
# /Single-post removal



# Whole-thread removal
class ThreadDeletion():
    """Table to represent whole-thread deletion events."""
    pass# TODO



class ThreadBan():
    """Table to represent whole-thread bans."""
    pass# TODO
    # Banned-by-username
    # Banned-by-user-id
    # Banned-by-usertype
    # Reason-text
    # reason-tags
    # ban-started
# /Whole-thread removal


# Single-image removal
class ImageDeletion():
    """Table to represent image deletion events."""
    pass# TODO



class ImageBan():
    """Table to represent image bans."""
    # size
    # md5
    # sha1
    # sha512
    # Banned-by-username
    # Banned-by-user-id
    # Banned-by-usertype
    # Reason-text
    # reason-tags
    # ban-started
    pass# TODO


class ImageHardBan():
    """Table to represent image hard bans."""
    # size
    # md5
    # sha1
    # sha512
    # Banned-by-username
    # Banned-by-user-id
    # Banned-by-usertype
    # Reason-text
    # reason-tags
    # ban-started
    pass# TODO
# /Single-image removal
#



def main():
    pass


if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "database_playground.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception as e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")