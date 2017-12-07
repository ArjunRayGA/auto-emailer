#!/usr/bin/env python

'''
MARKSTACHE
'''

__author__ = "Arjun Ray"
__credits__ = ["Arjun Ray"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Arjun Ray"
__email__ = "deconstructionalism@gmail.com"
__status__ = "development"

import json
import os
import re
import types

VALID_CONTEXT_TYPES = (types.NoneType, types.ComplexType, types.UnicodeType, types.LongType,
                       types.StringType, types.FloatType, types.IntType)

FILE_EXTENSIONS = {
    'markdown': [
        'markdown',
        'mdown',
        'mkdn',
        'md',
        'mkd',
        'mdwn',
        'mdtxt',
        'mdtext',
        'text',
        'Rmd'
        ],
    'json': [
        'json',
    ]
}

def markstache(file_path, root='', file_cache=None, file_extensions=FILE_EXTENSIONS,
               valid_context_types=VALID_CONTEXT_TYPES):
    '''
    returns CompileFile class instance of type for given file in filepath
    '''

    extension = file_path.split('.')[-1]
    file_class_name = "CompileFile"
    for file_type, extensions in file_extensions.iteritems():
        if extension in extensions:
            file_class_name = 'Compile{}{}File'.format(file_type[0].upper(), file_type[1:])
    compile_class = globals()[file_class_name]
    return compile_class(file_path, root, file_cache, file_extensions, valid_context_types)

class CompileFile(object):
    '''
    class for loading file text and compiling markstache tags within markdown and JSON files.
    accepts a file cache list of File classes.
    '''
    def __init__(self, file_path, root, file_cache, file_extensions, valid_context_types):
        assert isinstance(file_path, str), 'expected file_path as str but got {}' \
            .format(type(file_path))
        assert isinstance(root, str), 'expected root as str but got {}'.format(type(file_path))
        assert isinstance(file_cache, (list, types.NoneType)), \
            'expected file_cache as list but got {}' \
            .format(type(file_cache))
        if isinstance(file_cache, list):
            assert all([isinstance(e, File) for e in file_cache]), \
                'file_cache contains non-File elements: {}'.format([type(e) for e in file_cache])
        assert isinstance(file_extensions, dict), 'expected file_extension as dict but got {}' \
            .format(type(file_extensions))
        assert all([isinstance(val, list) for val in file_extensions.itervalues()]), \
            'file_extensions contains non-list elements: {}' \
            .format([type(e) for e in file_extensions])
        all_extensions = [ext for val in FILE_EXTENSIONS.itervalues() for ext in val]
        assert len(all_extensions) == len(set(all_extensions)), \
            'file_extensions contains shared extensions across file types'
        assert isinstance(valid_context_types, tuple), \
            'expected valid_context_types as tuple but got {}'.format(type(valid_context_types))
        assert all([isinstance(type_element, type) for type_element in valid_context_types]), \
            'non-type type passed to valid_context_types'

        self._file_cache = file_cache if file_cache else []
        self.file = None
        self._path = os.path.abspath(os.path.join(root, file_path))
        self.context = {}
        self.staches = {
            'matches': [],
            'renders': []

        }
        self._re = {
            'stache': re.compile(r'{{.*}}'),
            'ref': re.compile(r'^{{[\s\t]*_ref[\s\t]*=[\s\t]*(\(.*\)|[\'\"].*[\'\"])[\s\t]*}}$')
        }
        self._file_extensions = file_extensions
        self._valid_context_types = valid_context_types

    def process_file(self):
        '''
        processes File class based on whether it is a markdown file, JSON file, or other. In the
        first two cases, files are compiles based on markstache tags in file
        '''

        cache_paths = [f.path for f in self._file_cache]
        if self._path in cache_paths:
            self._finally()

        self._load_file()
        self._stache_search()
        self._compile()

        if len(self.staches['matches']) == 0:
            self._finally()


    def set_context(self, context=None):
        '''
        set the context dict for compilation
        '''

        assert isinstance(context, dict), 'expected context as dict but got {}' \
            .format(type(context))

        def _is_valid_type(var):
            '''
            check context dict recursively for invalid type in values
            '''

            if isinstance(var, dict):
                for key, val in var.iteritems():
                    if isinstance(val, dict):
                        _is_valid_type(val)
                    else:
                        assert isinstance(val, self._valid_context_types), \
                            'invalid type passed in context:\n    {}: {}'.format(key, type(val))

        try:
            _is_valid_type(context)
            self.context = context
        except AssertionError as error:
            raise AssertionError, str(error)



    def _stache_search(self):
        self.staches['matches'] = self._re['stache'].findall(self.file.contents)

    def _compile(self):
        for stache in self.staches['matches']:
            if re.match(self._re['ref'], stache):
                self.staches['renders'].append('s')
            else:
                to_eval = stache.strip().strip('{}')
                compile_context = self.context.copy()
                try:
                    eval_val = str(eval(to_eval, compile_context))
                except NameError as error:
                    eval_val = ''
                    raise NameError, '{} in context dict'.format(str(error))
                self.staches['renders'].append(eval_val)
        for i in range(len(self.staches['matches'])):
            if re.match(self._re['ref'], (self.staches['matches'][i]):
                
            self.file.contents = re.sub(self._re['stache'], self.staches['renders'][i],
                                        self.file.contents)

    def _load_file(self):
        self.file = File(self._path)
        self.file.load()

    def _finally(self):
        return self._file_cache



class File(object):
    '''
    class for loading contents from file_path as well as saving file extension and path information.
    takes a file_path string for path of file as well as root directory of file. also has utility
    functions for previewing file
    '''

    def __init__(self, path):
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

        print ('\n').join(self.contents.split('\n')[0:num_lines])
    def tail(self, num_lines=20):
        '''
        prints num_lines lines from end of file
        '''

        print ('\n').join(self.contents.split('\n')[-num_lines:])


class CompileJsonFile(CompileFile):
    '''
    File subclass that runs JSON file specific methods on __init__
    '''
    def __init__(self, file_path, root, file_cache, file_extensions,
                 valid_context_types):
        CompileFile.__init__(self, file_path, root, file_cache, file_extensions,
                             valid_context_types)
        print self.staches
        self._re["stache"] = \
            re.compile(r'(?:\".*\":)[\s](?![{])[\"][\s]*({{.*}})[\s]*[\"]')
    def _finally(self):
        self.file.contents = json.loads(self.file.contents)
        super(CompileJsonFile, self)._finally()

class CompileMarkdownFile(CompileFile):
    '''
    File subclass that runs JSON file specific methods on __init__
    '''
    def __init__(self, file_path, root, file_cache, file_extensions,
                 valid_context_types):
        CompileFile.__init__(self, file_path, root, file_cache, file_extensions,
                             valid_context_types)




if __name__ == '__main__':
    CACHE_FILE = File('../shared/markdown/not_a_real_file.txt')
    # CACHE_FILE.load()
    # MY_FILE = markstache('../shared/markdown/header.md', file_cache=[CACHE_FILE])
    MY_FILE = markstache('../templates/final_project_01/data.json', file_cache=[CACHE_FILE])
    # MY_FILE = markstache('../shared/data/class_data.json', file_cache=[CACHE_FILE])
    CONTEXT = {
        "str": "hi",
        "int": 1,
        "unicode": u'just',
        "none": None,
        "long": 65536*65536,
        "float": 22.33,
        "complex": complex(3, 4),
        "recipient": complex(3, 4),
        # "wrong": lambda x: x,
        "nested_dict": {
            "str": "hi",
            "int": 1,
            "unicode": u'just',
            "none": None,
            "long": 65536*65536,
            "float": 22.33,
            "complex": complex(3, 4),
            "nested_dict": {
                "str": "hi",
                "int": 1,
                "unicode": u'just',
                "none": None,
                "long": 65536*65536,
                "float": 22.33,
                "complex": complex(3, 4)
            }
        }
    }
    MY_FILE.set_context(CONTEXT)
    MY_FILE.process_file()
    print MY_FILE
    # print type(MY_FILE.file)
    # print MY_FILE.stache_matches
    # print MY_FILE.stache_renders
    print MY_FILE.file.contents
    print MY_FILE.staches
