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

def test_logger_extra():
    logger_name = 'test_name'
    TestMagicLogger = MagicLogger(logger_name=logger_name, file_name='test_output.txt', host=None, extra={"test": "test"})
    assert TestMagicLogger.extra.get("test")
    assert TestMagicLogger.extra["test"] == "test"

def test_log_extra():
    logger_name = 'test_name'
    TestMagicLogger = MagicLogger(logger_name=logger_name, file_name='test_output.txt', host=None,
                                  extra={"test": "test"})
    l = TestMagicLogger.error("random_message", extra = {"test": "test"})
    assert l.__dict__.get("test")
    assert l.__dict__["test"] == "test"


def test_decorate_extra():

    # @TestMagicLogger.decorate()
    # def test_function(x):
    #     import time
    #     time.sleep(2)
    #     return x
    # test_function(x=666)
    # print(TestMagicLogger)



    # os.remove('test_output.txt')
