#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `magic_logger` package."""

from magic_logger import MagicLogger
import os

def test_file_created():
    logger_name = 'test_name'
    TestMagicLogger = MagicLogger(logger_name=logger_name, file_name='test_output.txt', host=None)
    assert isinstance(TestMagicLogger, MagicLogger)
    test_message = 'test_message'
    TestMagicLogger.info(test_message)
    assert os.path.exists('test_output.txt') == True
    os.remove('test_output.txt')

def test_log_debug():
    logger_name = 'test_name'
    TestMagicLogger = MagicLogger(logger_name=logger_name, file_name='test_output.txt', host=None)
    test_message = 'test_message'
    TestMagicLogger.debug(test_message)

    with open('test_output.txt', 'r') as f:
        log_split = f.read().split(' - ')
        assert log_split[3].rstrip() == test_message
        assert log_split[2] == 'DEBUG'
        assert log_split[1] == logger_name

    os.remove('test_output.txt')

def test_log_info():
    logger_name = 'test_name'
    TestMagicLogger = MagicLogger(logger_name=logger_name, file_name='test_output.txt', host=None)
    test_message = 'test_message'
    TestMagicLogger.info(test_message)

    with open('test_output.txt', 'r') as f:
        log_split = f.read().split(' - ')
        assert log_split[3].rstrip() == test_message
        assert log_split[2] == 'INFO'
        assert log_split[1] == logger_name

    os.remove('test_output.txt')

def test_log_warning():
    logger_name = 'test_name'
    TestMagicLogger = MagicLogger(logger_name=logger_name, file_name='test_output.txt', host=None)
    test_message = 'test_message'
    TestMagicLogger.warning(test_message)

    with open('test_output.txt', 'r') as f:
        log_split = f.read().split(' - ')
        assert log_split[3].rstrip() == test_message
        assert log_split[2] == 'WARNING'
        assert log_split[1] == logger_name

    os.remove('test_output.txt')

def test_log_error():
    logger_name = 'test_name'
    TestMagicLogger = MagicLogger(logger_name=logger_name, file_name='test_output.txt', host=None)
    test_message = 'test_message'
    TestMagicLogger.error(test_message)

    with open('test_output.txt', 'r') as f:
        log_split = f.read().split(' - ')
        assert log_split[3].rstrip() == test_message
        assert log_split[2] == 'ERROR'
        assert log_split[1] == logger_name

    os.remove('test_output.txt')

def test_decorator():
    logger_name = 'test_name'
    TestMagicLogger = MagicLogger(logger_name=logger_name, file_name='test_output.txt', host=None)
    @TestMagicLogger.decorate()
    def test_function(x):
        return x
    test_function(x=666)

    os.remove('test_output.txt')


