#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Malcolm Ramsay <malramsay64@gmail.com>
#
# Distributed under terms of the MIT license.

"""
"""

from pathlib import Path

from logDirectory import LogDirectory

CWD = Path(__file__).parent
LOGDIR = CWD / 'test_log'

def test_file_list():
    log = LogDirectory(LOGDIR)
    assert len(log.file_list) == 27
    assert log.file_list == sorted(log.file_list, reverse=True)


def test_file_index():
    log = LogDirectory(LOGDIR)
    for index, filename in enumerate(log):
        print(index)
        assert log.get_file_index(filename) == index

def test_get_previous():
    log = LogDirectory(LOGDIR)
    prev_file = log.file_list[-1]
    # Reversing iterates in chronological order
    for filename in reversed(log):
        assert log.get_previous(filename) == prev_file
        prev_file = filename


def test_get_next():
    log = LogDirectory(LOGDIR)
    next_file = log.get_entry()
    for filename in log:
        assert log.get_next(filename) == next_file
        next_file = filename


def test_create_in():
    log = LogDirectory(LOGDIR)
    expected_index = (LOGDIR / 'expected_index.md').read_text()
    log.update_index()
    assert log.get_index().read_text() == expected_index
