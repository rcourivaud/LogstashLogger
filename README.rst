===============
Logstash Logger
===============


.. image:: https://img.shields.io/pypi/v/logstash_logger.svg
        :target: https://pypi.python.org/pypi/logstash_logger

.. image:: https://img.shields.io/travis/rcourivaud/logstash_logger.svg
        :target: https://travis-ci.org/rcourivaud/logstash_logger

.. image:: https://readthedocs.org/projects/logstash-logger/badge/?version=latest
        :target: https://logstash-logger.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/rcourivaud/logstash_logger/shield.svg
     :target: https://pyup.io/repos/github/rcourivaud/logstash_logger/
     :alt: Updates


Log handler to log better and send logs to Logstash

* Free software: MIT license
* Documentation: https://logstash-logger.readthedocs.io.


Features
--------

.. code-block:: bash

    pip install magic_logger

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

How to use
----------

1. Import module

.. code-block:: python

    from magic_logger import MagicLogger

2. Instantiate MagicLogger with a name. Logstash host is changed with kwarg `host`.
   If you have a specific Logstash host, feel free to edit the `magic_logger.py` default host.

.. code-block:: python

    logger = MagicLogger('Name', host='localhost')

3. Decorate a function in order to log it into Logstash and into the console

.. code-block:: python

    @logger.decorate('This is a message.')
    def a(*args, **kwargs):
        return 'This is a return'
    
    a('arg_1', 'arg_2', kwarg_1='hello', kwarg_2='world') 

Terminal output:

.. code-block:: bash

    2018-05-25 23:09:35,514 - Name - INFO - Connection to logstash successful.
    2018-05-25 23:09:35,518 - Name - DEBUG - This is a message.

Logstash output:

.. code-block:: bash

    logstash_1       | {
    logstash_1       |          "stack_info" => nil,
    logstash_1       |            "@version" => "1",
    logstash_1       |                "type" => "logstash",
    logstash_1       |             "message" => "This is a message.",
    logstash_1       |     "function_kwargs" => {
    logstash_1       |         "kwarg_2" => "world",
    logstash_1       |         "kwarg_1" => "hello"
    logstash_1       |     },
    logstash_1       |                "host" => "Nicolass-MacBook-Pro.local",
    logstash_1       |       "function_name" => "a",
    logstash_1       |                "path" => "/Users/nico/corners/MagicLogger/magic_logger/magic_logger.py",
    logstash_1       |               "class" => nil,
    logstash_1       |                "port" => 51772,
    logstash_1       |               "level" => "DEBUG",
    logstash_1       |                "tags" => [],
    logstash_1       |        "function_res" => "This is a return",
    logstash_1       |          "@timestamp" => 2018-05-25T21:09:35.518Z,
    logstash_1       |      "execution_time" => 5.0e-06,
    logstash_1       |         "logger_name" => "Name",
    logstash_1       |      "function_class" => nil
    logstash_1       | }

5. Add an extra to the decorator within the decorated function with the `update_extra` method

.. code-block:: python

    @logger.decorate('This is a message')
    def a():
        logger.update_extra(post_extra='This is a new extra')
        return 'This is a return'

    a()

6. Write a regular log

.. code-block:: python

    test_list = [1, 2, 3]
    test_string = "This is a string"
    logger.info('This is a message', extra = {"a_list": test_list, "a_string": test_string})

Terminal output:

.. code-block:: bash

    2018-05-25 17:08:15,654 - Name - INFO - This is a message

Logstash output:

.. code-block:: bash

    logstash_1       | {
    logstash_1       |      "@timestamp" => 2018-05-25T15:08:15.654Z,
    logstash_1       |         "message" => "This is a message",
    logstash_1       |            "type" => "logstash",
    logstash_1       |      "stack_info" => nil,
    logstash_1       |     "logger_name" => "Name",
    logstash_1       |            "path" => "test.py",
    logstash_1       |            "port" => 33542,
    logstash_1       |        "@version" => "1",
    logstash_1       |          "a_list" => [
    logstash_1       |         [0] 1,
    logstash_1       |         [1] 2,
    logstash_1       |         [2] 3
    logstash_1       |     ],
    logstash_1       |        "a_string" => "This is a string",
    logstash_1       |            "tags" => [],
    logstash_1       |            "host" => "MBP-C02WC1F4HV2Q.local",
    logstash_1       |           "level" => "INFO"
    logstash_1       | }

