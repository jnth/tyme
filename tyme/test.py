#!/usr/bin/env python3
# coding: utf-8

""" Test of Tyme. """

import os
import core
import configparser
import unittest
import tempfile


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


if __name__ == '__main__':
    unittest.main()

