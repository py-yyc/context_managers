import sys
import logging
import time
import math


if __name__ == "__main__":

    try:
        if sys.argv[1].startswith('c'):
            from two_timers import timer_class
            Timer = timer_class
            print "using timer class\n"
        else:
            raise RuntimeError()
    except:
        from two_timers import timer_decorator
        Timer = timer_decorator
        print "using timer decorator\n"

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

    with Timer('RuntimeError') as t:
        raise RuntimeError("uh oh")
    print t

    #with Timer('KeyError'):
    #    raise KeyError("uh oh")

    if False:
        n = 500
        with Timer("fast_fib") as t:
            f = fast_fib(n)
            print "fast_fib(%d) -> %s" % ( n, intcomma(f) )
            print "number of columns: %d" % math.log10(f)
        print t
