from cProfile import Profile
import pstats


def profile(sort_args=['cumulative'], print_args=[100]):
    profiler = Profile()

    def decorator(fn):
        def inner(*args, **kwargs):
            result = None
            try:
                result = profiler.runcall(fn, *args, **kwargs)
            finally:
                filename = _get_filename_for_function(fn)
                with open(filename, 'w') as stream:
                    stats = pstats.Stats(profiler, stream=stream)
                    stats.strip_dirs().sort_stats(*sort_args).print_stats(*print_args)
            return result
        return inner
    return decorator


def _get_filename_for_function(fn):
    function_name = fn.__module__ + "." + fn.__name__
    return function_name.replace(".", "_")
