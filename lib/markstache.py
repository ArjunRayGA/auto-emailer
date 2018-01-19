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

from markstache_modules.utils import File, FILE_CACHE
from markstache_modules.settings import FILE_EXTENSIONS, VALID_CONTEXT_TYPES
from markstache_modules.compile import CompileFile, CompileJsonFile, CompileMarkdownFile

def markstache(file_path, root='', file_extensions=FILE_EXTENSIONS,
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
    return compile_class(file_path, root, file_extensions, valid_context_types)


if __name__ == '__main__':
    CACHE_FILE = File('/Users/gafrontlines/auto-emailer/shared/markdown/headesdsr.md')
    FILE_CACHE.add_to_cache(CACHE_FILE)
    # MY_FILE = markstache('../shared/markdown/header.md')
    # MY_FILE = markstache('../templates/final_project_01/data.json')
    MY_FILE = markstache('../shared/data/class_data.json')
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
    print MY_FILE._stache_search
    # print MY_FILE
    # print type(MY_FILE.file)
    # print MY_FILE.stache_matches
    # print MY_FILE.stache_renders
    # print MY_FILE.file.contents
    # print MY_FILE.staches
    print FILE_CACHE.cache[1]
    print FILE_CACHE.cache[1].contents
