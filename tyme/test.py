#!/usr/bin/env python3
# coding: utf-8

""" Test of Tyme. """

import os
import configparser
import unittest
from unittest import mock
import tempfile
import io
import pkgutil
import tyme
import core
import notif


class TestConfig(unittest.TestCase):
    """ Test of configuration class. """

    def test_create_instance(self):
        """ Create instance of Config. """
        cfg = core.Config()
        self.assertEqual(cfg.sections, {})
        self.assertEqual(cfg.selected_cfgfile, None)
        self.assertEqual(cfg.fns[0], 'tyme.cfg')
        self.assertTrue(cfg.fns[1].endswith('.tyme.cfg'))

    def test_config_1section(self):
        """ Test of Config with one section. """
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            with open('tyme.cfg', 'w') as f:
                f.write("[spam]\negg = aZeRtY\nbacon = PoIuY\n\n")
            cfg = core.Config()
            cfg.read()
        self.assertEqual(list(cfg.sections.keys()), ['spam'])
        self.assertTrue('egg' in cfg.sections['spam'].keys())
        self.assertTrue('bacon' in cfg.sections['spam'].keys())
        self.assertEqual(cfg.sections['spam']['egg'], 'aZeRtY')
        self.assertEqual(cfg.sections['spam']['bacon'], 'PoIuY')

    def test_config_2sections(self):
        """ Test of Config with two sections. """
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            with open('tyme.cfg', 'w') as f:
                f.write("[foo]\nspam = 55\negg = 12\n\n[bar]\npy = 3\n\n")
            cfg = core.Config()
            cfg.read()
        self.assertTrue('foo' in cfg.sections.keys())
        self.assertTrue('bar' in cfg.sections.keys())
        self.assertTrue('spam' in cfg.sections['foo'].keys())
        self.assertTrue('egg' in cfg.sections['foo'].keys())
        self.assertTrue('py' in cfg.sections['bar'].keys())
        self.assertEqual(cfg.sections['foo']['spam'], '55')
        self.assertEqual(cfg.sections['foo']['egg'], '12')
        self.assertEqual(cfg.sections['bar']['py'], '3')

    def test_config_empty_file(self):
        """ Test of Config with empty configuration file. """
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            with open('tyme.cfg', 'w') as f:
                f.write("\n\n")
            cfg = core.Config()
            cfg.read()
        self.assertEqual(len(cfg.sections.keys()), 0)

    def test_config_no_file(self):
        """ Test of Config with no configuration file. """
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            cfg = core.Config()
            cfg.fns = []  # remove any reference to config path
            cfg.read()
        self.assertTrue('stderr' in cfg.sections.keys())
        self.assertEqual(len(cfg.sections['stderr']), 0)


class TestNotification(unittest.TestCase):
    """ Test of all notification class. """

    def test_notification(self):
        """ Test of notification class inside 'notif'. """
        modules = {
            modname: importer.find_module(modname).load_module(modname)
            for importer, modname, ispkg in pkgutil.iter_modules(notif.__path__)
            }
        for modname, m in modules.items():

            # Check the notification class name and number
            t = [e for e in dir(m) if e.startswith('Notification')]
            self.assertEqual(len(t), 1, "The file '%s.py' must contain only one class with a name beginning with 'Notification'" % modname)

            # Check the presence of methods 'send_ok' and 'send_error'
            cls = m.__dict__[t[0]]  # link to the class object
            inst = cls(**{'spam': 'AzerTY', 'egg': 'NbvFhk'})  # inject dict
            self.assertIn('send_ok', dir(inst),
                          "A 'send_ok' must be present in the '%s' class" % cls.__name__)
            self.assertIn('send_error', dir(inst),
                          "A 'send_error' must be present in the '%s' class" % cls.__name__)
            self.assertEqual(inst.spam, 'AzerTY')
            self.assertEqual(inst.egg, 'NbvFhk')


class TestTyme(unittest.TestCase):
    """ Test of Tyme class. """

    def create_config(self, d, outdir):
        """ Create configuration file.
        :param d: {'section': {'key1': 'option1', ...}}
        :param outdir: path of output directory.
        """
        cfgp = configparser.ConfigParser()
        cfgp.read_dict(d)
        with open(os.path.join(outdir, 'tyme.cfg'), 'w') as f:
            cfgp.write(f)

    def test_tyme_ok(self):
        """ Test with a success command. """
        patched_stdout = mock.patch('sys.stdout', new_callable=io.StringIO)
        patched_stderr = mock.patch('sys.stderr', new_callable=io.StringIO)
        with patched_stderr as stderr, patched_stdout as stdout:
            with tempfile.TemporaryDirectory() as tmpdir:
                os.chdir(tmpdir)
                self.create_config({'stderr': {}}, tmpdir)
                t = tyme.Tyme()
                self.assertEqual(list(t.notifs.keys()), ['stderr'])
                rc = t.run("exit")
                self.assertEqual(rc, 0)
        stdout.seek(0)
        stderr.seek(0)
        self.assertEqual(len(stdout.read()), 0)
        self.assertEqual(stderr.read().strip(),
                         "[tyme: command `exit` executed successfully]")

    def test_tyme_error(self):
        """ Test with a error command. """
        patched_stdout = mock.patch('sys.stdout', new_callable=io.StringIO)
        patched_stderr = mock.patch('sys.stderr', new_callable=io.StringIO)
        with patched_stderr as stderr, patched_stdout as stdout:
            with tempfile.TemporaryDirectory() as tmpdir:
                os.chdir(tmpdir)
                self.create_config({'stderr': {}}, tmpdir)
                t = tyme.Tyme()
                self.assertEqual(list(t.notifs.keys()), ['stderr'])
                rc = t.run("exit 9")
                self.assertEqual(rc, 9)
        stdout.seek(0)
        stderr.seek(0)
        self.assertEqual(len(stdout.read()), 0)
        self.assertEqual(stderr.read().strip(),
                         "[tyme: command `exit 9` failed (error no 9)]")


if __name__ == '__main__':
    unittest.main()

