#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `magic_logger` package."""

from magic_logger import MagicLogger
import os

TestMagicLogger = MagicLogger(logger_name='test_name', file_name='test_output.txt', host=None)

def test_file_created():
    assert isinstance(TestMagicLogger, MagicLogger)
    test_message = 'test_message'
    TestMagicLogger.info(test_message)
    assert os.path.exists('test_output.txt') == True

    # with open('test_output.txt', 'r') as f:
    #     assert f.read().strip('\n') == test_message


    # os.remove('test_output.txt')
def test_file_log():
    test_message = 'test_message'
    TestMagicLogger.info()

