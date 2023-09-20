import os
import sys

# Utils
def join(*paths):
    """ Join paths and normalize the result."""
    return os.path.normpath(os.path.join(*paths))


def add_to_path(*rel_path):
    path = join(__file__, "..", *rel_path)
    sys.path.insert(0, path)


add_to_path("src")
