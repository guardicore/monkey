import os
import pstats
from cProfile import Profile

PROFILER_LOG_DIR = "./profiler_logs/"


def profile(sort_args=['cumulative'], print_args=[100]):

    def decorator(fn):
        def inner(*args, **kwargs):
            result = None
            try:
                profiler = Profile()
                result = profiler.runcall(fn, *args, **kwargs)
            finally:
                try:
                    os.mkdir(PROFILER_LOG_DIR)
                except os.error:
                    pass
                filename = PROFILER_LOG_DIR + _get_filename_for_function(fn)
                with open(filename, 'w') as stream:
                    stats = pstats.Stats(profiler, stream=stream)
                    stats.strip_dirs().sort_stats(*sort_args).print_stats(*print_args)
            return result
        return inner
    return decorator


def _get_filename_for_function(fn):
    function_name = fn.__module__ + "." + fn.__name__
    return function_name.replace(".", "_")
