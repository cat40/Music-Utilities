import os
import numpy
import shutil
import cPickle as pickle
#from exceptions import *
#from exceptions import exceptions.CacheNotFoundError #fix import problem later
#import exceptions


numpyexts = ('.npy', '.npz')
pickleext = '.pkl'

class exceptions(object):
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

'''
class to manage caching. Note that arbitrary code can be executed when loading pickled objects
very strongly consider handling numpy arrays the same as everything else, becuase it is quite likley more trouble than it's worth to manage the file extensions, and confusing
when the end user saves under 'name' and loads under 'name.npy'. Also avoids the problem of the user needing to know if the data is a numpy array before loading
'''
class Cache(object):
    def __init__(self, cachepath):
        self._path = cachepath
        try: os.makedirs(self._path)
        except OSError as e:
            pass #fix later
##            if e.errno != e.errno.EEXIST:
##                raise

    '''
    writes a single object to the cache under file 'name'
    '''
    def write(self, data, name):
        if isinstance(data, numpy.ndarray):
            numpy.save(self.genfname(name+'.npy'), data)
        else:
            with open(self.genfname(name), 'w') as f:
                pickle.dump(data, f)

    '''
    write a group of objects to the cache under thier respective names
    datas is a list of tuples in the form (object, name)
    '''
    def writeBatch(self, *datas):
        for data, name in datas:
            self.write(data, name)

    '''
    load a file under the name fname as an object
    rasies exceptions.CacheNotFoundError if the file does not exist
    '''
    def load(self, fname):
        fname = self.genfname(fname)
        try:
            if self.isNumpy(fname):
                return numpy.load(self.genfname(fname))
            with open(fname) as f:
                return pickle.load(f)
        except IOError, e:
            if e.errno == 2: #file not found
                raise exceptions.CacheNotFoundError(fname + ' was not found in the cache directory ' + self._path) #note: this still creates a race condition, but this way it can be fixed for all implimenttaions at once
            else:
                raise

    '''
    load all files in the cache. Returns a dictionary of the form {name : object}
    '''
    def loadall(self):
        #currently assumes a flat directory. will fix this later
        data = {}
        for fname in os.listdir(self._path):
            data[fname] = self.load(fname)
        return data

    '''
    deletes a file from the cache
    '''
    def delete(self, fname):
        os.remove(self.genfname(fname))

    '''
    clears the cache by delting all files
    '''
    def clear(self):
        for fname in os.listdir(fname):
            fname = self.genfname(fname)
            if os.path.isdir(fname):
                shutil.rmtree(fname)
            else:
                os.remove(fname)

    '''
    destorys the cache by deleting the cache directory
    '''
    def destroy(self):
        shutil.rmtree(self._path)
        del self # this doesn't actually do anything, but it looks cool

    '''
    checks if a file is in the cache
    Do not use this to see if a file exists before trying to load it because that creates a race condition
    Instead use a try-except statement catching the exceptions.CacheNotFoundError. 
    '''
    def exists(self, fname): #consider replacing this with a custom exception for use in try-except statements
        return os.path.isfile(self.genfname(fname)) if isNumpy(fname) else os.path.isfile(self.genfname(fname+pickleext))

    @staticmethod
    def isNumpy(fname):
        return os.path.splitext(fname)[1] in numpyexts

    #this is here in case the name generatrion method changes
    def genfname(self, fname):
        if self.isNumpy(fname):
            return os.path.join(self._path, fname)
        return os.path.join(self._path, fname+pickleext)
