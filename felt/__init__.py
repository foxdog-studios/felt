# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pipes
import re

from fabric.api import *

from pathlib import PurePath


class Command(object):
    def __init__(self, *arguments):
        self.arguments = []
        self << arguments

    def __iter__(self):
        return iter(self.arguments)

    def __str__(self):
        return self.get_command()

    def append(self, argument):
        self.arguments.append(self.escape(argument))
    __lt__ = append

    def extend(self, arguments):
        for argument in arguments:
            self < argument
    __lshift__ = extend

    def make_command(self):
        return ' '.join(self.arguments)

    def run(self, *args, **kwargs):
        if kwargs.pop('use_sudo', False):
            runner = sudo
        else:
            runner = run
        return runner(self.make_command(), *args, **kwargs)

    def sudo(self, *args, **kwargs):
        kwargs['use_sudo'] = True
        return self.run(*args, **kwargs)

    @classmethod
    def run_cmd(cls, *arguments, **run_kwargs):
        return cls(*arguments).run(**run_kwargs)

    @staticmethod
    def escape(argument):
        return pipes.quote(unicode(argument))


def margin(text):
    return re.sub(r'^ *\|', '', text.strip(), flags=re.MULTILINE)


def mkdir(directories, mode=None, parents=False, verbose=False, **kwargs):
    cmd = Command('/usr/bin/mkdir')
    if mode is not None:
        cmd < '--mode={mode}'.format(mode=mode)
    if parents:
        cmd < '--parents'
    if verbose:
        cmd < '--verbose'
    if isinstance(directories, PurePath):
        directories = [directories]
    cmd << directories
    return cmd.run(**kwargs)


def mv(sources, destination, **kwargs):
    cmd = Command('/usr/bin/mv')
    if isinstance(sources, PurePath):
        sources = [sources]
    cmd << sources
    cmd < destination
    return cmd.run(**kwargs)


def rm(files, force=False, recursive=False, verbose=False, **kwargs):
    cmd = Command('/usr/bin/rm')
    if force:
        cmd < '--force'
    if recursive:
        cmd < '--recursive'
    if verbose:
        cmd < '--verbose'
    if isinstance(files, PurePath):
        files = [files]
    cmd << files
    return cmd.run(**kwargs)

