#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `magic_logger` package."""

from magic_logger import MagicLogger
import os

def test_file_created():
    TestMagicLogger = MagicLogger(logger_name='test_name', file_name='test_output.txt', host=None)
    assert isinstance(TestMagicLogger, MagicLogger)
    test_message = 'test_message'
    TestMagicLogger.info(test_message)
    assert os.path.exists('test_output.txt') == True
    os.remove('test_output.txt')

def test_log_info():
    TestMagicLogger = MagicLogger(logger_name='test_name', file_name='test_output.txt', host=None)
    test_message = 'test_message'
    TestMagicLogger.info(test_message)

    with open('test_output.txt', 'r') as f:
        # assert f.read().split(' - ')[3].rstrip() == test_message
        assert f.read().split(' - ')[2] == 'INFO'

    os.remove('test_output.txt')
