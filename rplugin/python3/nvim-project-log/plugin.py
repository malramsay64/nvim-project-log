#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Malcolm Ramsay <malramsay64@gmail.com>
#
# Distributed under terms of the MIT license.

import datetime
from pathlib import Path
from typing import List, Iterator

import neovim


class LogDir(object):
    def __init__(self, directory: str) -> None:
        self.directory = Path(directory)
        self.index = 'index.md'

    @property
    def file_list(self) -> List[Path]:
        return list(self)

    def __iter__(self) -> Iterator[Path]:
        return dist(self.directory.glob('????-??-??.md'))

    def get_index(self) -> str:
        return str(self.directory / self.index)

    def get_entry(self) -> str:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        return str(self.directory / '{date}.md'.format(date=today))

    def get_file_index(self, filename: Path) -> int:
        """Get the position of the current file within the list."""
        for index, fname in enumerate(self):
            if fname == filename:
                return index

    def 


@neovim.plugin
class Main(object):
    def __init__(self, vim) -> None:
        self.vim = vim
        directories = ['~/notes']
        try:
            directories = self.vim.api.get_var('project_log#logbooks')
        except OSError:
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
