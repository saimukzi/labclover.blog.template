import hashlib
import os
import pathlib

from urllib.parse import urljoin as _urljoin

def find_file(dir):
    """Recursively finds all files in a directory.

    Args:
        dir (str): The directory to search.

    Returns:
        list: A list of full paths to all files found.
    """
    file_list = []
    for root, _, files in os.walk(dir):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def read_file(fn, encoding='utf-8'):
    """Reads a file and returns its lines.

    Args:
        fn (str): The path to the file.
        encoding (str, optional): The file encoding. Defaults to 'utf-8'.

    Returns:
        list: A list of strings, where each string is a line from the file.
    """
    with open(fn, 'rt', encoding=encoding) as fin:
        ret = fin.readlines()
    ret = [i.strip('\n') for i in ret]
    return ret

def md5(text):
    """Calculates the MD5 hash of a string.

    Args:
        text (str): The string to hash.

    Returns:
        str: The MD5 hash of the string.
    """
    return hashlib.md5(text.encode(encoding='utf-8')).hexdigest()

def md5_file(fn):
    """Calculates the MD5 hash of a file.

    Args:
        fn (str): The path to the file.

    Returns:
        str: The MD5 hash of the file.
    """
    with open(fn, 'rb') as fin:
        data = fin.read()
    return hashlib.md5(data).hexdigest()

def is_file_equal(fn1, fn2):
    """Checks if two files are equal.

    Args:
        fn1 (str): The path to the first file.
        fn2 (str): The path to the second file.

    Returns:
        bool: True if the files are equal, False otherwise.
    """
    with open(fn1, 'rb') as fin:
        data1 = fin.read()
    with open(fn2, 'rb') as fin:
        data2 = fin.read()
    return data1 == data2

def to_native_path(path):
    """Converts a path to the native path format.

    Args:
        path (str): The path to convert.

    Returns:
        str: The path in the native format.
    """
    return str(pathlib.PurePath(path))

def to_rel_url(path):
    """Converts a path to a relative URL.

    Args:
        path (str): The path to convert.

    Returns:
        str: The relative URL.
    """
    parts = pathlib.PurePath(path).parts
    return '/'.join(parts)

def native_path_to_posix(npath):
    """Converts a native path to a POSIX path.

    Args:
        npath (str): The native path to convert.

    Returns:
        str: The POSIX path.
    """
    npath = os.path.abspath(npath)
    return pathlib.Path(npath).as_posix()

def urljoin(*args):
    """Joins multiple parts of a URL together.

    This function is similar to `urllib.parse.urljoin`, but it can join
    more than two parts at once.

    Args:
        *args: The parts of the URL to join.

    Returns:
        str: The joined URL.
    """
    ret = args[0]
    for i in args[1:]:
        if not ret.endswith('/'):
            ret += '/'
        ret = _urljoin(ret, i)
    return ret
