#-------------------------------------------------------------------------------
# Name:        media_fetcher.py
# Purpose:  Code for media fetcher threads
#
# Author:      Ctrl-S
#
# Created:     07-04-2019
# Copyright:   (c) Ctrl-S 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------


def process_one_todo_image(db_ses, db_row, remove_failed=True):# TODO; WIP
    """TODO
    Take one image from the TODO queue and save it if possible.
    Remove the item from the queue once done.
    if remove_failed is True: Remove items from todo if DL fails for any reason.
    """


    pass

def download_some_images(db_ses, pk_list):# TODO; WIP
    """pk_range should be a list of primary keys that have been exclusively allocated to this function."""
    for pk in pk_list:
        # Open row
        # Download for row
        # Mark row as finished




def image_dl_loop(board_name, db_ses):# TODO; WIP
    loop_counter = 0
    while (True):
        loop_counter += 1
        logging.debug('Image DL loop {0}'.format(loop_counter))
        # Grab a batch of images
        # Allocate batch to DL handlers
        # Attempt to save one image
        process_one_todo_image(db_ses, remove_failed=True)


def prune_finished_todo_rows(db_ses, todo_table, board_name, minimum_age_hours_to_remove=24):# TODO; WIP
    # Calculate datetime for age comparison
    # Select some rows where both age > minimum and done == True
    # Delete returned rows
    return


def downloader_thread_main(db_ses, board_name):# TODO; WIP
    """Root of an image download thread."""



def main():
    pass

if __name__ == '__main__':
    main()
