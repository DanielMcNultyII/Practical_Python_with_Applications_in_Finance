'''
Daniel McNulty II

This module contains the Memoize function
'''


# Import partial from the functools module
from functools import wraps


# memoize function
def memoize(f):
    # Initialize an empty dict to hold previously calculated values and store it in variable _memo
    _memo = {}

    # Use @wraps to allow for the function f to be seen when using its __repr__ function
    @wraps(f)
    # Nesting functions, creating function wrapper() that wraps around the function f. Uses *args in order to work with
    # functions with any number of input parameters
    def wrapper(*args):
        # Check if the input args are not within the cache dict _memo
        if args not in _memo:
            # If the input args are not, create a new entry in the cache dict _memo with keyword args and store the
            # result of passing args into the passed in function within it.
            _memo[args] = f(*args)

        # Return the value stored in cache dict _memo for keyword args.
        return _memo[args]
    # Decorator syntax requires you to return the wrapped function within the outer function.
    return wrapper
