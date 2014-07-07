# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from cStringIO import StringIO
import json
import pipes
import re

from fabric.api import *

from pathlib import PurePath

import yaml

from felt import systemctl
from felt.command import Command


def chown(*args, **kwargs):
    cmd = Command('/usr/bin/chown')
    def pop(key):
        return kwargs.pop(key, False)
    if pop('recursive'):
        cmd < '--recursive'
    if pop('verbose'):
        cmd < '--verbose'
    parts = []
    if 'owner' in kwargs:
        parts.append(kwargs.pop('owner'))
    if 'group' in kwargs:
        parts.append(':')
        parts.append(kwargs.pop('group'))
    cmd < ''.join(parts)
    cmd << args
    return cmd.run(**kwargs)


def ln(*args, **kwargs):
    def pop(key):
        return kwargs.pop(key, False)
    cmd = Command('/usr/bin/ln')
    if pop('force'):
        cmd < '--force'
    if pop('symbolic'):
        cmd < '--symbolic'
    if pop('no_target_directory'):
        cmd < '--no-target-directory'
    cmd << args
    return cmd.run(**kwargs)


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


def nginx_escape(param):
    return "'{}'".format(param
        .replace('\\', r'\\')
        .replace('$' , r'\$')
        .replace("'" , r'\'')
    )


def put_str(str_, remote_path, *args, **kwargs):
    return put(StringIO(str_), str(remote_path), *args, **kwargs)


def read(path):
    with path.open() as file_:
        return file_.read()


def read_json(path):
    with path.open() as file_:
        return json.load(file_)


def read_yaml(path):
    with path.open() as file_:
        return yaml.load(file_)


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

