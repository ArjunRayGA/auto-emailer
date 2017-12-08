#!/usr/bin/env python

'''
settings for markstache

WARNING: do not add extension data to FILE_EXTENSIONS unless you follow these rules:
    * key name is a single word
    * you have created a CompileKeynameFile class in compile.py and imported it into markstache.py
    * that value is a list with only extensions as strings, with no shared extensions between keys
'''

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
