import logging
import time
from contextlib import contextmanager

@contextmanager
def timer_decorator(prefix=''):

    start =  time.time()

    try:
        yield ''
    except Exception as e:
        logging.warn( "NOT swallowing exception: %s", str(e) )
        raise
    finally:
        delta = time.time() - start
        print "%s took %f secs" % (prefix, delta)
        print


class timer_class(object):

    def __init__(self, prefix=''):
        """
        this is a normal object and can take initialization parameters
        """
        self._prefix = prefix

    def __enter__(self):
        """
        the value returned by this method is bound to the identifier in
        the as clause of with statements using this context manager.
        """
        self._start =  time.time()
        return self

    def __exit__( self, exc_type, exc_val, exc_traceback):
        """
        return True to cause caller to continue happily
        return False to cause caller to reraise passed in exception
        """

        # print timings no matter what
        self._end = time.time()

        if exc_type is not None:    # uh oh! exception happened
            # we could handle the exception if we knew how
            # here is an example...
            if exc_type is RuntimeError:
                logging.warn( "swallowing exception: %s", str(exc_val) )
                return True

            return False            # return False to cause caller to re-raise exception

        return True

    def __str__(self):
        delta = self._end - self._start
        return "%s took %f secs\n" % (self._prefix, delta)

