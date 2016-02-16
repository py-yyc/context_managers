import logging
import time
import math

class Timer(object):

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
                logging.warn( "swallowing exception: %s\n", str(exc_val) )
                return True

            return False            # return False to cause caller to re-raise exception

        return True

    def __str__(self):
        delta = self._end - self._start
        return "%s took %f secs\n" % (self._prefix, delta)


if __name__ == "__main__":

    from humanize import intcomma
    from lib import slow_fib, fast_fib

    n = 35

    with Timer("slow_fib") as t:
        f = slow_fib(n)
        print "slow_fib(%d) -> %s" % ( n, intcomma(f) )
    print t

    with Timer("fast_fib") as t:
        f = fast_fib(n)
        print "fast_fib(%d) -> %s" % ( n, intcomma(f) )
    print t

    with Timer('RuntimeError'):
        raise RuntimeError("uh oh")

    #with Timer('KeyError'):
    #    raise KeyError("uh oh")

    if True:
        n = 500
        with Timer("fast_fib") as t:
            f = fast_fib(n)
            print "fast_fib(%d) -> %s" % ( n, intcomma(f) )
            print math.log10(f)
        print t
