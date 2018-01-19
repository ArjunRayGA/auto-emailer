#!/usr/bin/env python

'''
compile methods and classses for markstache
'''

import json
import os
import re
from utils import File, FILE_CACHE

class CompileFile(object):
    '''
    class for loading file text and compiling markstache tags within markdown and JSON files.
    accepts a file cache list of File classes.
    '''
    def __init__(self, file_path, root, file_extensions, valid_context_types):
        assert isinstance(file_path, str), \
            'expected file_path as str but got {}' \
            .format(type(file_path))
        assert isinstance(root, str), \
            'expected root as str but got {}' \
            .format(type(file_path))
        assert isinstance(file_extensions, dict), \
            'expected file_extension as dict but got {}' \
            .format(type(file_extensions))
        assert all([isinstance(val, list) for val in file_extensions.itervalues()]), \
            'file_extensions contains non-list elements: {}' \
            .format([type(e) for e in file_extensions])
        all_extensions = [ext for val in file_extensions.itervalues() for ext in val]
        assert len(all_extensions) == len(set(all_extensions)), \
            'file_extensions contains shared extensions across file types'
        assert isinstance(valid_context_types, tuple), \
            'expected valid_context_types as tuple but got {}' \
            .format(type(valid_context_types))
        assert all([isinstance(type_element, type) for type_element in valid_context_types]), \
            'non-type type passed to valid_context_types'

        # self._file_cache = file_cache if file_cache else []
        self.file = None
        self.__path = os.path.abspath(os.path.join(root, file_path))
        self.context = {}
        self.staches = {
            'matches': [],
            'renders': []
        }
        self.__re = {
            'stache': re.compile(r'{{.*}}'),
            'ref': re.compile(r'^{{[\s\t]*_ref[\s\t]*=[\s\t]*(\(.*\)|[\'\"].*[\'\"])[\s\t]*}}$')
        }
        self.__file_extensions = file_extensions
        self.__valid_context_types = valid_context_types

    def process_file(self):
        '''
        processes File class based on whether it is a markdown file, JSON file, or other. In the
        first two cases, files are compiles based on markstache tags in file
        '''

        cache_paths = [f.path for f in FILE_CACHE.cache]
        if self.__path in cache_paths:
            return

        self._load_file()
        self._stache_search()
        if len(self.staches['matches']) == 0:
            self._finally()
            return
        self._compile()
        self._finally()

    def set_context(self, context=None):
        '''
        set the context dict for compilation
        '''

        assert isinstance(context, dict), \
            'expected context as dict but got {}' \
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
                        assert isinstance(val, self.__valid_context_types), \
                            'invalid type passed in context:\n    {}: {}'.format(key, type(val))

        try:
            _is_valid_type(context)
            self.context = context
        except AssertionError as error:
            raise AssertionError, str(error)

    def _set_re(self, re_name, re_regex):
        assert isinstance(re_name, str), \
            'expected re_name as str but got {}' \
            .format(type(re_name))
        assert isinstance(re_regex, re._pattern_type), \
            'expected re_regex as regex object but got {}' \
            .format(type(re_regex))
        self.__re[re_name] = re_regex

    def _stache_search(self):
        self.staches['matches'] = self.__re['stache'].findall(self.file.contents)

    def _compile(self):
        for stache in self.staches['matches']:
            if re.match(self.__re['ref'], stache):
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
            # if re.match(self.__re['ref'], (self.staches['matches'][i]):

            self.file.contents = re.sub(self.__re['stache'], self.staches['renders'][i],
                                        self.file.contents)

    def _load_file(self):
        self.file = File(self.__path)
        self.file.load()

    def _finally(self):
        FILE_CACHE.add_to_cache(self.file)

class CompileJsonFile(CompileFile):
    '''
    File subclass that runs JSON file specific methods on __init__
    '''
    def __init__(self, file_path, root, file_extensions,
                 valid_context_types):
        CompileFile.__init__(self, file_path, root, file_extensions, valid_context_types)
        ref_re = re.compile(r'(?:\".*\":)[\s](?![{])[\"][\s]*({{.*}})[\s]*[\"]')
        self._set_re('ref', ref_re)
    def _finally(self):
        self.file.contents = json.loads(self.file.contents)
        super(CompileJsonFile, self)._finally()

class CompileMarkdownFile(CompileFile):
    '''
    File subclass that runs JSON file specific methods on __init__
    '''
    def __init__(self, file_path, root, file_extensions, valid_context_types):
        CompileFile.__init__(self, file_path, root, file_extensions, valid_context_types)
