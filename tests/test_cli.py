"""Tests for our main task5 CLI module."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

from task5 import __version__ as VERSION


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['task5', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)

        output = popen(['task5', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['task5', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), VERSION)
