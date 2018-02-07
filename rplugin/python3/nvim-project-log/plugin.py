#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Malcolm Ramsay <malramsay64@gmail.com>
#
# Distributed under terms of the MIT license.

import logging
from pathlib import Path

import neovim

from .logDirectory import LogDirectory

logger = logging.getLogger('nvim-project-log')
logger.setLevel(logging.DEBUG)

@neovim.plugin
class Main(object):

    def __init__(self, vim) -> None:
        self.vim = vim
        self._set_log_status()
        directories = ['~/notes']
        try:
            directories = self.vim.api.get_var('project_log#logbooks')
        except OSError:
            directories = ['~/notes']
        self.log_dirs = [LogDirectory(directory) for directory in directories]
        self.current_index = 0

    def _set_log_status(self) -> None:
        root = logging.getLogger('nvim-project-log')
        handler = logging.FileHandler(filename='/Users/malcolm/project_log.log')
        root.addHandler(handler)
        root.setLevel(logging.DEBUG)
        logstatus = self.vim.api.get_var('project_log#log_level')
        log_level = getattr(logging, logstatus, logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG, filename='/tmp/nvim-project-log.log')
        logger.debug('Setting log level to %s', log_level)

    @property
    def current_log(self) -> LogDirectory:
        return self.log_dirs[self.current_index]

    def num_log_dirs(self) -> int:
        return len(self.log_dirs)

    def update_current_index(self, count) -> None:
        # Handle error condition
        if count > self.num_log_dirs():
            self.error('[Count] of {} is outside range of logbooks.'.format(count))
            return
        # Count specified -> update current index
        if count > 0:
            self.current_index = count - 1

    def error(self, message: str) -> None:
        """Handle error messages in a consitent fashion."""
        self.vim.command('echohl WarningMsg | echo "{}" | echohl None'.format(message))

    @neovim.command('ProjectLogIndex', count=-1)
    def open_index(self, count: int) -> None:
        """Navigate to the index of the logbook."""
        self.update_current_index(count)
        # Open index file
        self.vim.command('edit {}'.format(self.current_log.get_index()))

    @neovim.command('ProjectLogToday', count=-1)
    def open_entry(self, count: int) -> None:
        self.update_current_index(count)
        # Open index file
        self.vim.command('edit {}'.format(self.current_log.get_entry()))

    @neovim.command('ProjectLogPrevious')
    def project_log_previous(self) -> None:
        current_file = Path(self.vim.current.buffer.name)
        self.vim.command('edit {}'.format(self.current_log.get_previous(current_file)))

    @neovim.command('ProjectLogNext')
    def project_log_next(self) -> None:
        current_file = Path(self.vim.current.buffer.name)
        self.vim.command('edit {}'.format(self.current_log.get_next(current_file)))

    @neovim.command('ProjectLogUpdateIndex')
    def project_log_update_index(self) -> None:
        self.current_log.update_index()
