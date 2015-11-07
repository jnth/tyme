#!/usr/bin/env python3
# coding: utf-8

""" __Tyme__ : notify me when a command is finished. """


from core import BaseNotification
import smtplib
from email.mime.text import MIMEText


# The notification class name must start with `Notification`.
# This class must have :
#   - an `__init__` function with a **kwargs argument.
#   - an `send_ok` function.
#   - an `send_error` function with the error code in argument.
#
# ** Be careful ! **  
# All options in configuration file in the corresponding section
# will be passed in the `__init__` function as string kwargs.


class NotificationGmail(BaseNotification):
    def __init__(self, **kwargs):
        BaseNotification.__init__(self, **kwargs)  # do not change this line

    def send_email(self, title, message):
        """ Send a email.
        :param title: title.
        :param message: message body.
        """
        msg = MIMEText(message)
        msg['From'] = self.login
        msg['To'] = self.addr_to
        msg['Subject'] = title

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.login, self.password)
        s.sendmail(self.login, self.addr_to.split(','), msg.as_string())
        s.quit()

    def send_ok(self):
        self.send_email("Command executed successfully",
                        "Command `{cmd}` is terminated".format(cmd=self.cmd))

    def send_error(self, errno):
        self.send_email("Command failed",
                        "Command `{cmd}` failed with error no {e}".format(
                            cmd=self.cmd, e=errno))

