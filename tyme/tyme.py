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
import logging
import subprocess
import configparser
import pkgutil
import notif
import core


# Debug mode if TYME_DEBUG is set in environnement variable
loglvl = logging.DEBUG if 'TYME_DEBUG' in os.environ else logging.WARNING

# Log
logging.basicConfig(level=loglvl,
                    format="[%(asctime)s] %(levelname)8s | %(message)s")
log = logging  # alias
log.info("starting tyme.py")

# Class
class Tyme(object):
    """ Tyme: notify me when my command is done. """

    def __init__(self):
        self.read_config()

    def read_config(self):
        """ Read configuration. """
        # Read configuration and get section names
        cfg = core.Config()
        cfg.read()
        log.info("selected config file : %s" % cfg.selected_cfgfile)

        # Load submodule
        modules = {
            modname: importer.find_module(modname).load_module(modname)
            for importer, modname, ispkg in pkgutil.iter_modules(notif.__path__)
            if modname in cfg.sections.keys()
        }
        log.info("load submodule : %s" % list(modules.keys()))

        # Create notification instance for each activated submodule
        self.notifs = dict()
        for modname, m in modules.items():
            t = [e for e in dir(m) if e.startswith('Notification')]

            if not len(t):
                raise SystemError(("The '{modname}' module must contain a "
                                   "'Notification...' class").format(**locals()))

            if len(t) > 1:
                raise SystemError(("The '{modname}' module must contain only one "
                                   "'Notification...' class").format(**locals()))

            cls = m.__dict__[t[0]]  # class
            kw = cfg.sections[modname]  # dict from configuration
            self.notifs[modname] = cls(**kw)  # new instance

    def run(self, cmd):
        """ Run a command.
        :param cmd: command with or without arguments and options as string.
        :return: return code of command as integer.
        """

        # Run command and notify
        log.debug("start running command...")
        proc = subprocess.run(cmd, shell=True)
        log.debug("end of command with return code %i" % proc.returncode)

        for modname, notif in self.notifs.items():
            notif.cmd = cmd  # add command name inside instance
            if proc.returncode == 0:
                notif.send_ok()
                log.info("success notification '%s' done" % modname)
            else:
                notif.send_error(proc.returncode)
                log.info("error notification '%s' done" % modname)

        # Return the command return code
        return proc.returncode


if __name__ == '__main__':

    # Read arguments
    cmd = sys.argv[1:]

    if not cmd:  # test with 'echo'
        cmd = "echo 'test of tyme'"
    else:
        cmd = " ".join(cmd)
    log.info("command to run : %s" % cmd)

    # Start Tyme
    tyme = Tyme()
    rc = tyme.run(cmd)

    # Exit with the command return code
    log.info("end of tyme.py")
    sys.exit(rc)

