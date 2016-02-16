import logging
import time

from contextlib import contextmanager

@contextmanager
def Timer(prefix=''):

    start =  time.time()

    try:
        yield
    except Exception as e:
        logging.warn( "NOT swallowing exception: %s", str(e) )
        raise
    finally:
        delta = time.time() - start
        print "%s took %f secs" % (prefix, delta)
        print

if __name__ == "__main__":

    from humanize import intcomma
    from lib import slow_fib, fast_fib

    n = 3

    with Timer("slow_fib"):
        f = slow_fib(n)
        print "slow_fib(%d) -> %s" % ( n, intcomma(f) )
    print

    with Timer("fast_fib"):
        f = fast_fib(n)
        print "fast_fib(%d) -> %s" % ( n, intcomma(f) )
    print

    with Timer('runtime error'):
        raise RuntimeError("uh oh")

    if False:
        n = 500
        with Timer("fast_fib"):
            f = fast_fib(n)
            print "fast_fib(%d) -> %s" % ( n, intcomma(f) )
            print math.log10(f)
