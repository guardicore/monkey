import unicodedata
import six

__author__ = 'itay.mizeretz'


def byteify_str(unicode_str):
    """
    Converts a unicode string to ascii string.
    :param unicode_str: A unicode string
    :return: Converted ascii string.
    """
    return unicodedata.normalize('NFKD', unicode_str).encode('ascii', 'ignore')


def byteify(unicode_input):
    """
    Deep converts unicode strings in object to ascii strings.
    :param unicode_input: Any object which may contain unicode strings
    :return: Same as input with ascii strings instead of unicode.
    """
    if isinstance(unicode_input, dict):
        return {byteify(key): byteify(value) for key, value in six.iteritems(unicode_input)}
    elif isinstance(unicode_input, list):
        return [byteify(element) for element in unicode_input]
    elif isinstance(unicode_input, unicode):
        return byteify_str(unicode_input)
    else:
        return unicode_input
