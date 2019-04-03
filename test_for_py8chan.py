#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      me
#
# Created:     03-04-2019
# Copyright:   (c) me 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------





class Thread(object):
    """Represents a thread.

    Attributes:
        closed (bool): Whether the thread has been closed.
        sticky (bool): Whether this thread is a 'sticky'.
        topic (:class:`py8chan.Post`): Topic post of the thread, the OP.
        posts (list of :class:`py8chan.Post`): List of all posts in the thread, including the OP.
        all_posts (list of :class:`py8chan.Post`): List of all posts in the thread, including the OP and any omitted posts.
        url (string): URL of the thread, not including semantic slug.

	Undefined Attributes (Not implemented in 8chan API. Do not use.):
        replies and images: Infuriatingly, the OP post in a thread
        doesn't list how many replies there are in a thread.
        semantic_url (string): URL of this post, with the thread's 'semantic' component.
        semantic_slug (string): This post's 'semantic slug'.
    """
    def __init__(self, board, id):
        self.id = self.number = self.num = self.no = id
        self.topic = None
        self.replies = []
        self.is_404 = False
        self.last_reply_id = 0
        self.omitted_posts = 0
        self.omitted_images = 0
        self.want_update = False

    def __len__(self):
        return self.num_replies

    @property
    def id(self):
        return self.id

    @property
    def number(self):
        return self.id

    @property
    def num(self):
        return self.id

    @property
    def no(self):
        return self.id







def main():
    pass

if __name__ == '__main__':
    main()
