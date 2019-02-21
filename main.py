# Main.py
# Playground for now, later it can be something 
# Imports
# stdlib
import os
import logging
import re
# Remote libraries
# Local modules
import common
import config

# Load a thread from the API





# We want to pull threads from the API and store them
# We want to compare the latest thread data to the saved thread data
# We want to compare posts
# We want to keep track of what images we've saved
# We want to save images we don't have



# Long term datastructures:
# Postgres DB?
# Fields:
# Banned: "This shit will not touch my server, under any circumstances."
# Deleted: "Nobodies eyes may glimpse this."

# TABLE %BOARD%_threads
# int thread_num, JSONB posts, boolean deleted, boolean banned,

# TABLE %BOARD%_media
# unicode disk_path_full, disk_path_thumb, disk_path_opthumb, unicode md5b64, unicode sha1b64, unicode sha512b64, int size, boolean deleted, boolean banned,


# TABLE %BOARD%_thumbs

# TABLE %BOARD%_deleted
# unicode md5b64, unicode sha1b64, unicode sha512b64, int size, unicode reason, unicode deleted_by, 

# TABLE global_media

# TABLE global_thumbs






def main():
    pass


if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "main.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception as e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")