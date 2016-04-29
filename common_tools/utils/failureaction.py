
"""
====================
Failureaction Readme
====================

This package is intended to provide decorators which execute custom actions
in case of exceptions. Let's see an example:

First we need an object with some methods. These methods we decorate with
the *PrintOnFailure*-decorator. This simple example decorator prints a given
message in case of an exception.

    from failureaction import ConflictError
    from failureaction import PrintOnFailure
    class TestOb(object):
  ...
        @PrintOnFailure(msg='Some numeric calculation went wrong!')
        def divide(self, a, b):
            return a/b

        @PrintOnFailure()
  ...   def doraise(self):
  ...       raise ConflictError

We have two methods. One (divide) does numerical division of two numbers
and another raises a custom defined ConflictError. Now let's see the methods in
action:

   ob = TestOb()
   ob.divide(4, 2)
  2

   ob.divide(42, 0)
  Some numeric calculation went wrong!

   ob.doraise()
  Traceback (most recent call last):
  ...
  ConflictError

The *ActionOnFailure* decorator provided by the module is intended to be
overriden by a custom class. Like this:

    from failureaction import ActionOnFailure
    class MailOnFailure(ActionOnFailure):
   ...
...     def __init__(self, subject):
...         self.subject = subject
...
...     def _doaction(self, context, e):
...         # send a mail, if an exception was raised
...         print "Subject:", self.subject
...         print e

    class TestOb2(object):
   ...
        @MailOnFailure(subject='An error occured')
        def critical(self):
   ...      import _not_existent_hopefully_

    ob2 = TestOb2()
    ob2.critical()
    Subject: An error occured
    No module named _not_existent_hopefully_

"""

import sys
try:
    from ZODB.POSException import ConflictError
except ImportError:
    # we don't want to depend on Zope here, this package is generally usable

    class ConflictError(Exception):
        """ A dummy ConflictError """

class ActionOnFailure(object):
    """ A decorator for doing an action in case of an exception.
    """

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ConflictError, KeyboardInterrupt), e:
                raise
            except Exception, e:
                context = args[0]
                return self._doaction(context, e)
        self.func = func
        wrapper.__name__ = func.__name__
        wrapper.__dict__.update(func.__dict__)
        wrapper.__doc__ = func.__doc__
        return wrapper

    def _doaction(self, context, e):
        raise NotImplementedError


class PrintOnFailure(ActionOnFailure):
    """ Print something in case of an exception.
    """

    def __init__(self, msg='foo'):
        self.msg = msg

    def _doaction(self, context, e):
        print self.msg

# Selftest

class TestOb(object):

    @PrintOnFailure(msg='foo bar')
    def doaction(self):
        1/0

    @PrintOnFailure()
    def doraise(self):
        raise ConflictError

if __name__ == '__main__':
    ob = TestOb()
    ob.doaction()
    ob.doraise()
