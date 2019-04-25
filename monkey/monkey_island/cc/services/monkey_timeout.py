import functools
import pprint


def start_timer_decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        print("ib4get - start the timer, folks. \nargs:")
        pprint.pprint(args)
        print("kwargs: ")
        pprint.pprint(kwargs)
        value = func(*args, **kwargs)
        print("after party woohoo")

        try:
            print("Starting timer on " + kwargs['guid'])
        except KeyError as e:
            print("NO GUID AVAILABLE")

        return value

    return wrapper_decorator
