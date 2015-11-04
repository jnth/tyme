#!/usr/bin/env python3
# coding: utf-8

"""
__Tyme__: notify me when a command is finished.

Usage: tyme.py [command [args]...]
"""

__version__ = '0.1'
__author__ = 'jnth'


import os
import sys
import subprocess
import configparser
import pkgutil
import notif


# Open configuration
#  1st: 'tyme.cfg' in current directory
#  2nd: '.tyme.cfg' in $HOME directory
#  3rd: basic configuration by default
if os.path.isfile('tyme.cfg'):
    fncfg = 'tyme.cfg'
elif os.path.isfile(os.path.join(os.environ['HOME'], '.tyme.cfg')):
    fncfg = os.path.join(os.environ['HOME'], '.tyme.cfg')
else:
    pass


# Read configuration and get section names
cfg = configparser.ConfigParser()
cfg.read(fncfg)
sections = cfg.sections()

# Load submodule
modules = {
    modname: importer.find_module(modname).load_module(modname)
    for importer, modname, ispkg in pkgutil.iter_modules(notif.__path__)
    if modname in sections
}

# Create notification instance for each activated submodule
notifs = dict()
for modname, m in modules.items():
    t = [e for e in dir(m) if e.startswith('Notification')]

    if not len(t):
        raise SystemError(("The '{modname}' module must contain a "
                           "'Notification...' class").format(**locals()))

    if len(t) > 1:
        raise SystemError(("The '{modname}' module must contain only one "
                           "'Notification...' class").format(**locals()))

    cls = m.__dict__[t[0]]  # class
    kw = dict(cfg[modname].items())  # dict from configuration
    notifs[modname] = cls(**kw)  # new instance


# Read arguments
cmd = sys.argv[1:]

if not cmd:  # test with 'echo'
    cmd = "echo 'test of tyme'"
else:
    cmd = " ".join(cmd)

# Run command and notify
proc = subprocess.run(cmd, shell=True)
for modname, notif in notifs.items():
    notif.cmd = cmd  # add command name inside instance
    if proc.returncode == 0:
        notif.send_ok()
    else:
        notif.send_error(proc.returncode)

# Exit with the command return code
sys.exit(proc.returncode)
