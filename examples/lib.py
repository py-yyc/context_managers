def slow_fib( n ):
    if n <= 2:
        return 1

    return slow_fib(n-2) + slow_fib(n-1)

def fast_fib( n ):
    """
    http://bosker.wordpress.com/2011/04/29/the-worst-algorithm-in-the-world/

    this is so fast that you don't even need to memoize it
    loop_fibonacci(2500) is .000453 or .000001 with memoize
    fast_fibonacci(2500) is .000022 or .000001 with memoize
    """
    def bits(n):
        """Represent an integer as an array of binary digits.
        """
        bits = []
        while n > 0:
            n, bit = divmod(n, 2)
            bits.append(bit)
        bits.reverse()
        return bits

    assert n >= 0
    a, b, c = 1, 0, 1
    for bit in bits(n):
        if bit:
            a, b = (a+c)*b, b*b + c*c
        else:
            a, b = a*a + b*b, (a+c)*b

        c = a + b

    return b
