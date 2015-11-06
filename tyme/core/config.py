#!/usr/bin/env python3
# coding: utf-8

""" __Tyme__ : notify me when a command is finished. """


import os
from configparser import ConfigParser


class Config(object):
    def __init__(self):
        self.sections = {}
        self.fns = [
            'tyme.cfg',
            os.path.join(os.environ['HOME'], '.tyme.cfg')
        ]
        self.selected_cfgfile = None

    def _find_cfg_file(self):
        return [e for e in self.fns if os.path.isfile(e)]

    def _read_cfg(self, fn):
        cfg = ConfigParser()
        cfg.read(fn)
        sections = cfg.sections()
        for sect in sections:
            self.sections[sect] = dict(cfg[sect].items())

    def read(self):
        fncfgs = self._find_cfg_file()
        if not fncfgs:
            self.sections['stderr'] = {}  # default config
        else:
           self._read_cfg(fncfgs[0])  # read 1st config file found
           self.selected_cfgfile = fncfgs[0]

