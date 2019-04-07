#-------------------------------------------------------------------------------
# Name:        assert2
# Purpose: A better assert()
#
# Author:      Ctrl-S
#
# Created:     07-04-2019
# Copyright:   (c) Ctrl-S 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import unittest






def assert2(exp, msg=None, value=None):# THIS IS A DISTRACTION! LEAVE IT BE!
    """Custom Assert function.
    exp: Assert fires if not True.
    msg: Message explaining the assertion to be logged along with the value when assert fires.

    Basically assert() except should dump information about value.
    PREMISE: Trust noone, each function should verify what it gets from elsewhere just ot be fucking damn sure. This does not excuse the original data not being to spec, only excuses us from blame for propogating the fuckup.
    TODO: Make PEP for better builtin assertions; look for existing better assertions;
    """
    if (not exp):
        # Assertion failed
        logging.error('ASSERT2 FIRED WITH MESSAGE: {0}'.format(msg))
        logging.error('ASSERT2 FIRED WITH value: {0!r}'.format(value))
        raise AssertionError()
    return


class test_displayed_datatypes(unittest.TestCase):
    def test_list_of_strings(self):
        pass# TODO




def main():
    unittest.main()

if __name__ == '__main__':
    main()
