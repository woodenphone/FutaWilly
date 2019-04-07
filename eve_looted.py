#! /usr/bin/python3
# Expects python 3.x
#-------------------------------------------------------------------------------
# Name:        eve_looted
# Purpose: Code i grabbed from bianon's eve project
#
# Author:      Ctrl-S
#
# Created:     08-04-2019
# Copyright:   (c) Ctrl-S 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------






class MediaFetcher(object):
    """Handles media downloads for a single board. Instantiated by each Board.

    doesn't support the old directory structure; does anyone care?"""
    def __init__(self, board):
        super(MediaFetcher, self).__init__()
        self.mediaDLQueue = eventlet.queue.Queue()
        self.selectMediaQuery = selectMediaQuery.format(board = board)
        self.board = board

        eventlet.spawn(self.fetcher)

    def put(self, post):
        self.mediaDLQueue.put(post)

    def fetcher(self):
        while True:
            post = self.mediaDLQueue.get()
            logger.debug('fetching media %s', post['md5'])
            if getattr(config, "downloadMedia", False):
                self.download(post['no'], post['resto'] == 0, False, post['tim'], post['ext'], post['md5'])
            if getattr(config, "downloadThumbs", False):
                self.download(post['no'], post['resto'] == 0, True, post['tim'], post['ext'], post['md5'])
            self.mediaDLQueue.task_done()
            utils.status()

    def download(self, postNum, isOp, isPreview, tim, ext, mediaHash):
        #Local.java:198

        #Get metadata from DB
        with connectionPool.item() as conn:
            c = conn.cursor()
            result = c.execute(self.selectMediaQuery, (mediaHash,))
            assert result == 1
            mediaRow = MediaRow(*c.fetchone())

        if mediaRow.banned:
            logger.info('Skipping download of banned file ', mediaHash)
            return

        #determine filename
        #   Added to DB by insert_image_<board> procedure - triggered by before-ins-<board>
        if isPreview:
            filename = mediaRow.preview_op if isOp else mediaRow.preview_reply
        else:
            filename = mediaRow.media

        #if(filename == null) return;
        if filename == None:
            logger.warning("media download failed to determine destination filename")
            logger.warning("post {} hash {}".format(postNum, mediaHash))
            return

        #make directories
        subdirs = (filename[:4], filename[4:6])
        destinationFolder = "{}/{}/{}/{}".format(config.imageDir+"/"+self.board, "thumb" if isPreview else "images", *subdirs) #FIXME use os.path.join
        os.makedirs(destinationFolder, exist_ok = True) #TODO maybe just skip this and use os.renames at the end?

        #set perms on directories
        #TODO

        #determine final file path, and bail if it already exists
        destinationPath = destinationFolder + os.sep + filename
        if os.path.exists(destinationPath):
            logger.debug('skipping download of already downloaded media')
            logger.debug("post {} hash {}".format(postNum, mediaHash))
            return

        #download the URL into a tempfile
        tmp = tempfile.NamedTemporaryFile(delete = False) #FIXME handle leaks on error
        url = "https://i.4cdn.org/{}/{}{}{}".format(self.board, tim, "s" if isPreview else "", ".jpg" if isPreview else ext)

        while True:
            delay = 5
            try:
                logger.debug('fetching media: post {} hash {}'.format(postNum, mediaHash))
                request = cfScraper.get(url)
                request.raise_for_status()
                break
            except Exception as e:
                if isinstance(e, erequests.HTTPError):
                    if request.status_code == 404: #404s are to be expected, just bail when they happen
                        logger.info("404 when downloading media")
                        logger.info("post {} hash {}".format(postNum, mediaHash))
                        return
                # log everything else and try again
                logger.warning('{} while fetching media post {} hash {}, will try again in {} seconds'.format(e.__class__.__name__, postNum, mediaHash, delay))
                logger.warning('exception args: '+repr(e.args)) #not sure how useful this will be
                eventlet.sleep(delay)
                delay = min(delay + 5, 300)
                continue

        for chunk in request.iter_content(chunk_size=1024*512):
            tmp.write(chunk)
        tmp.close()

        #move the tempfile to the final file path
        shutil.move(tmp.name, destinationPath)

        #set permissions on file path
        #webGroupId is never set in asagi, so should we even do this? Is this even relevant today?
        # os.chmod(destinationPath, 0o644)
        #posix.chown(outputFile.getCanonicalPath(), -1, this.webGroupId);
        logger.debug('downloaded media: {}/{}'.format(self.board, filename))










def main():
    pass

if __name__ == '__main__':
    main()
