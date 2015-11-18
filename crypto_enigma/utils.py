#!/usr/bin/env python
# encoding: utf8

# Copyright (C) 2015 by Roy Levien.
# This file is part of crypto-enigma, an Enigma Machine simulator.
# released under the BSD-3 License (see LICENSE.txt).

"""
Description

.. note::
    Any additional note.
"""

from __future__ import (absolute_import, print_function, division, unicode_literals)

import time
import sys


# TBD - Generalize to other platforms; test?
def print_over(s, delay=0.2):
    print(s, end='\r')
    print("\033[F" * (s.count('\n')+1))
    sys.stdout.flush()
    time.sleep(delay)


def num_A0(c):
    return ord(c) - ord('A')


def chr_A0(n):
    return chr(n + ord('A'))


def ordering(items):
    return [i[1] for i in sorted(zip(items, range(0, len(items))))]


# standard simple-substitution cypher encoding
def encode_char(mapping, ch):
    if ch == ' ':
        return ' '
    else:
        return mapping[num_A0(ch)]


def encode_string(mapping, string):
    return ''.join([encode_char(mapping, ch) for ch in string])


# scan, because it's missing from Python; implemented to anticipate Python 3
def accumulate(l, f):
    it = iter(l)
    total = next(it)
    yield total
    for element in it:
        total = f(total, element)
        yield total


# also missing from Python
def chunk_of(it, n):
    return [it[i:i+n] for i in range(0, len(it), n)]


# require unicode strings - http://stackoverflow.com/a/33743668/656912
def require_unicode(*given_arg_names):
    def check_types(_func_, *args):
        def modified(*args):
            arg_names = list(_func_.func_code.co_varnames[:_func_.func_code.co_argcount])
            if len(given_arg_names) == 0:
                unicode_arg_names = arg_names
            else:
                unicode_arg_names = given_arg_names
            for unicode_arg_name in unicode_arg_names:
                try:
                    arg_index = arg_names.index(unicode_arg_name)
                except ValueError:
                    raise NameError, unicode_arg_name
                arg = args[arg_index]
                if not isinstance(arg, unicode):
                    raise TypeError("Parameter '{}' should be a Unicode literal".format(unicode_arg_name))
            return _func_(*args)
        return modified
    return check_types