#!/usr/bin/env python

'''
utils for markstache
'''

class File(object):
    '''
    class for loading contents from file_path as well as saving file extension and path information.
    takes a file_path string for path of file as well as root directory of file. also has utility
    functions for previewing file
    '''

    def __init__(self, path):

        assert isinstance(path, str), \
            'expected path as str but got {}' \
            .format(type(path))

        self.path = path
        self.extension = path.split('.')[-1]
        self.type = 'text'
        self.contents = ''
    def load(self):
        '''
        save file at file_path contents to self.contents
        '''

        try:
            with open(self.path, 'r') as open_file:
                self.contents = open_file.read()
        except IOError:
            raise IOError, '"{}" does not exist'.format(self.path)
    def head(self, num_lines=20):
        '''
        prints num_lines lines from beggining of file
        '''

        print(('\n').join(self.contents.split('\n')[0:num_lines]))
    def tail(self, num_lines=20):
        '''
        prints num_lines lines from end of file
        '''

        print(('\n').join(self.contents.split('\n')[-num_lines:]))


class FileCache(object):
    '''
    cache for storing File class objects
    '''

    def __init__(self):
        self.cache = []

    def add_to_cache(self, file_obj):
        '''
        add File class object to class
        '''

        assert isinstance(file_obj, File), \
            'expected file_obj as File class object but got {}' \
            .format(type(file_obj))

        self.cache.append(file_obj)

FILE_CACHE = FileCache()
