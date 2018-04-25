'''
base class for cache related errors
'''
class CacheError(Exception):
    pass


'''
used when the file being request does not exist
'''
class CacheNotFoundError(CacheError):
    pass


