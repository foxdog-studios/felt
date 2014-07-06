# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from felt.command import Command


__all__ = ['reload']


def reload(name):
    return Command.run_cmd(
        '/usr/bin/systemctl',
        'reload',
        name,
        use_sudo=True,
    )

