#!/usr/bin/env python3
# coding: utf-8

""" __Tyme__ : notify me when a command is finished. """


from sys import stderr


# The notification class name must start with `Notification`.
# This class must have :
#   - an `__init__` function with a **kwargs argument.
#   - an `send_ok` function.
#   - an `send_error` function with the error code in argument.
#
# ** Be careful ! **
# All options in configuration file in the corresponding section
# will be passed in the `__init__` function as string kwargs.


class NotificationStderr(object):
    def __init__(self, **kwargs):
        self.cmd = None  # will be completed later...

    def send_ok(self):
        stderr.write("[tyme: command `{cmd}` executed successfully]\n".format(
            cmd=self.cmd))

    def send_error(self, errno):
        stderr.write("[tyme: command `{cmd}` failed (error no {e})]\n".format(
            cmd=self.cmd, e=errno))

