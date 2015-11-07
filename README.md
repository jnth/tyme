# Tyme

**Tyme** is an acronyme to *notify me* when a command is finished.


## Why ?

I need to know when a long running script is finished as soon as possible. So, I created this program to that purpose.


## How ?

Use it in front of any command.

    tyme.py a_long_running_script.sh --with-arguments

By default, it's only use stderr to show the status of the command.  
But, you can create a configuration file to use specific notification (push with Pushover, email, ...)

### Create a configuration

`Tyme` will search configuration file :

  - named `tyme.cfg` in the current directory,
  - named `.tyme.cfg` in the `HOME` directory.

If any configuration file is found, it will use stderr to notify the end of the task.

Each section inside the configuration file represents a notification process. A corresponding python file must be present inside the `notif` directory with a specific class name (start with `Notification`) and methods (`send_ok` and `send_error`).

Each options inside a section will be passed to create an instance of the notification class. This is used to define login, password or keys (see `notif/pushover.py` for example).

### Create a notification

First, you need to create a python script inside the `notif` directory with a `Notification` class based on `BaseNotification`.

For this example, we will create `notif.gmail.py` and add a Gmail Notification in it with, a least, `send_ok` and `send_error` methods :

```python
from core import BaseNotification
import smtplib
from email.mime.text import MIMEText

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
        s.sendmail(self.login, self.addr_to, msg.as_string())
        s.quit()

    def send_ok(self):
        self.send_email("Command executed successfully",
                        "Command `{cmd}` is terminated".format(cmd=self.cmd))

    def send_error(self, errno):
        self.send_email("Command failed",
                        "Command `{cmd}` failed with error no {e}".format(
                            cmd=self.cmd, e=errno))
```

In this example, we add another method `send_email` to send an email without duplicate this part of code.

Test this new class :

```bash
./test.py
```

These tests only check if your new class if correct (name of class and methods). It does not check code inside methods !

Create or alter a configuration file with this section :

```cfg
[gmail]
login = my.email@home.com
password = my_secret_password
addr_to = my.email@work.com, another.email@somewhere.com
```

The section title must match the python file in `notif` directory.
Option names in this section must match variable of the new class.

Test it with debug mode :

```bash
TYME_DEBUG=1 ./tyme.py
```

In the log, you can see the use of this new notification system :

```log
[2015-11-07 14:52:39]     INFO | starting tyme.py
[2015-11-07 14:52:39]     INFO | command to run : echo 'test of tyme'
[2015-11-07 14:52:39]     INFO | selected config file : tyme.cfg
[2015-11-07 14:52:41]     INFO | load submodule : ['gmail', 'stderr']
[2015-11-07 14:52:41]    DEBUG | start running command...
test of tyme
[2015-11-07 14:52:41]    DEBUG | end of command with return code 0
[2015-11-07 14:52:43]     INFO | success notification 'gmail' done
[tyme: command `echo 'test of tyme'` executed successfully]
[2015-11-07 14:52:43]     INFO | success notification 'stderr' done
[2015-11-07 14:52:43]     INFO | end of tyme.py
```

## Note

A debug mode (verbose mode) can be activated if you set a `TYME_DEBUG` environnement variable.

This script is under developpement...  
It's missing a complete documentation and tests with different python version and OS. See [TODO](TODO.md) file.

For now, it's running ok with python 3.5 on linux.

