#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Malcolm Ramsay <malramsay64@gmail.com>
#

import datetime
from pathlib import Path
from typing import List, Iterator

import logging

logger = logging.getLogger('nvim-project-log')
logger.setLevel(logging.DEBUG)


class LogDirectory(object):
    def __init__(self, directory: str) -> None:
        self.directory = Path(directory)
        self.index = 'index.md'

    @property
    def _files(self):
        return self.directory.glob('????-??-??.md')

    @property
    def file_list(self) -> List[Path]:
        return list(self)

    def __iter__(self) -> Iterator[Path]:
        yield self.get_entry()
        for file in sorted(list(self._files), reverse=True):
            if file != self.get_entry():
                yield file

    def __reversed__(self) -> Iterator[Path]:
        for file in sorted(list(self._files), reverse=False):
            if file != self.get_entry():
                yield file
        yield self.get_entry()

    def __len__(self) -> int:
        return len(list(self._file_list))

    def get_index(self) -> Path:
        return self.directory / self.index

    def get_entry(self) -> Path:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        return self.directory / '{date}.md'.format(date=today)

    def get_file_index(self, filename: Path) -> int:
        """Get the position of the current file within the list."""
        logger.debug('Finding index of %s in dir %s', filename.name, filename.parent)
        for index, iter_fname in enumerate(self):
            iter_fname = Path(iter_fname)
            logger.debug('  Index: %s, filename: %s', index, iter_fname.name)
            if iter_fname.name == filename.name:
                return index
        raise IndexError('{} was not found'.format(filename))

    def get_previous(self, filename: Path) -> Path:
        """Get previous file in chronologically in list.

        This will attempt to find the previous function by date, ensuring
        that should an error arise like a lack of elements in the list,
        or attempting to go through the boundaries of the list that a sensible
        result is returned.

        """
        try:
            current_index = self.get_file_index(filename)

            logger.debug('Current index: %s', current_index)
            return self.file_list[current_index + 1]
        except IndexError:
            logger.debug('Current index not found.')
            # Check there are elements in the list
            if self.file_list:
                # The last item is the oldest
                return self.file_list[-1]
            # return entry for today
            return self.get_entry()

    def get_next(self, filename: Path) -> Path:
        """Get previous file in chronologically list."""
        try:
            current_index = self.get_file_index(filename)
            if current_index == 0:
                # At start of list return entry from current day
                return self.get_entry()
            return self.file_list[self.get_file_index(filename) - 1]
        except IndexError:
            # Check there are elements in the list
            if self.file_list:
                # The zeroth item is the most recent
                return self.file_list[0]
            # Return the entry for today
            return self.get_entry()

    def update_index(self):
        """Add all the files to the index as links labelled by the first line."""
        index_string = 'Index\n=====\n\n'
        for logfile in self:
            with logfile.open() as src:
                index_string += '- [{label}]({link})\n'.format(label=src.readline().strip(),
                                                               link=logfile.name)
        with self.get_index().open('w') as dst:
            dst.write(index_string)
