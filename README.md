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

Each section inside the configuration file represents a notification process. A corresponding python file must be present inside the `notif` directory with a specific class name and methods.

Each options inside a section will be passed to create an instance of the notification class. This is used to define login, password or keys (see `notif/pushover.py` for example).


## Note

A debug mode (verbose mode) can be activated if you set a `TYME_DEBUG` environnement variable.

This script is under developpement...  
It's missing a complete documentation and tests with different python version and OS. See [TODO](TODO.md) file.

For now, it's running ok with python 3.5 on linux.

