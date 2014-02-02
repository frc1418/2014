

def enum(**enums):
    '''From http://stackoverflow.com/a/1695250'''
    return type('Enum', (), enums)


def is_iterable(o):
    try:
        iter(o)
    except TypeError:
        return False
    else:
        return True
