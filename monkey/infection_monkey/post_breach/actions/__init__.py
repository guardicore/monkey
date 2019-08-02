from os.path import dirname, basename, isfile, join
import glob


def get_pba_files():
    """
    Gets all files under current directory(/actions)
    :return: list of all files without .py ending
    """
    files = glob.glob(join(dirname(__file__), "*.py"))
    return [basename(f)[:-3] for f in files if isfile(f) and not f.endswith('__init__.py')]
