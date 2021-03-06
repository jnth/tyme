#!/usr/bin/env python3
# coding: utf-8

""" __Tyme__ : notify me when a command is finished. """


from core import BaseNotification
import requests


# The notification class name must start with `Notification`.
# This class must have :
#   - an `__init__` function with a **kwargs argument.
#   - an `send_ok` function.
#   - an `send_error` function with the error code in argument.
#
# ** Be careful ! **  
# All options in configuration file in the corresponding section
# will be passed in the `__init__` function as string kwargs.


class NotificationStderr(BaseNotification):
    def __init__(self, **kwargs):
        BaseNotification.__init__(self, **kwargs)  # do not change this line
        self.url_post = "https://api.pushover.net/1/messages.json"

    def push(self, title, message):
        """ Send push.
        :param title: title.
        :param message: message body.
        """
        data = dict(
            token=self.app_token,
            user=self.user_key,
            title=title,
            message=message,
        )
        requests.post(self.url_post, data=data)

    def send_ok(self):
        self.push("Command executed successfully",
                  "Command `{cmd}` is terminated".format(cmd=self.cmd))

    def send_error(self, errno):
        self.push("Command failed",
                  "Command `{cmd}` failed with error no {e}".format(
                      cmd=self.cmd, e=errno))

