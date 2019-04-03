#-------------------------------------------------------------------------------
# Name:        fuckups.py
# Purpose:    Local exception classes
#
# Author:      Ctrl-S
#
# Created:     30-03-2019
# Copyright:   (c) Ctrl-S 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------




class FuckUp(Exception):
    """
    Local exception superclass.
    Someone fucked up.
    Something went wrong and we need to signal that fact.
    """
    pass# Nothing to do in an exception class like this other than hold a name.


class WeFuckedUp(FuckUp):
    """
    We fucked up.
    Something went wrong with this code.
    Bad coder.
    See RFC 7231 section 6.6 at https://tools.ietf.org/html/rfc7231#section-6.6
    """
    pass# Nothing to do in an exception class like this other than hold a name.



class YouFuckedUp(FuckUp):
    """
    You fucked up.
    Something went wrong that is all the user's fault.
    Bad user.
    See RFC 7231 section 6.5 at https://tools.ietf.org/html/rfc7231#section-6.5
    """
    pass# Nothing to do in an exception class like this other than hold a name.



class TheyFuckedUp(FuckUp):
    """
    The Man fucked up.
    Something went wrong that is neither this code's nor the user's fault.
    Goddamnit.
    """
    pass# Nothing to do in an exception class like this other than hold a name.



class AssertAFuckupHappened(FuckUp, AssertionError):
    """
    Something got fucked up and we noticed.
    This is basically an Assertion replacement.
    """
    pass# Nothing to do in an exception class like this other than hold a name.



class DeliberateDevelopmentFuckup(Fuckup):
    """
    A deliberate fuckup, introduced for development reasons.
    Intended to be implimented merely temporary.
    If a user experiences this Fuckup then we have fucked up too hard.
    """
    pass# Nothing to do in an exception class like this other than hold a name.





def main():
    pass

if __name__ == '__main__':
    main()
