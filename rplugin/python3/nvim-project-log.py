#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Malcolm Ramsay <malramsay64@gmail.com>
#
# Distributed under terms of the MIT license.

import datetime
from pathlib import Path

import neovim


class LogDir(object):
    def __init__(self, directory: str) -> None:
        self.directory = Path(directory)
        self.index = 'index.md'

    def get_index(self) -> str:
        return str(self.directory / self.index)

    def get_entry(self) -> str:
        now = datetime.datetime.now()
        return '{date}.md'.format(date=now.strftime('%Y-%m-%d'))


@neovim.plugin
class Main(object):
    def __init__(self, vim) -> None:
        self.vim = vim
        directories = ['~/notes']
        self.log_dirs = [LogDir(directory) for directory in directories]
        self.current_index = 0

    def get_current_log(self) -> LogDir:
        return self.log_dirs[self.current_index]

    def num_log_dirs(self):
        return len(self.log_dirs)

    def error(self, message: str) -> None:
        """Handle error messages in a consitent fashion."""
        self.vim.command('echohl WarningMsg | echo "{}" | echohl None'.format(message))

    @neovim.command('ProjectLogIndex', count=-1)
    def open_index(self, count: int) -> None:
        """Navigate to the index of the logbook."""
        # Handle error condition
        if count > self.num_log_dirs():
            self.error('[Count] of {} is outside range of logbooks.'.format(count))
            return
        # Count specified -> update current index
        if count > 0:
            self.current_index = count - 1
        # Open index file
        self.vim.command('edit {}'.format(self.get_current_log().get_index()))

    @neovim.command('ProjectLogToday', count=-1)
    def open_entry(self, count: int) -> None:
        # Handle error condition
        if count > self.num_log_dirs():
            self.error('[Count] of {} is outside range of logbooks.'.format(count))
            return
        # Count specified -> update current index
        if count > 0:
            self.current_index = count - 1
        # Open index file
        self.vim.command('edit {}'.format(self.get_current_log().get_entry()))
