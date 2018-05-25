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

    logger = MagicLogger('Name')

3. Decorate a function in order to log it into Logstash and into the console

.. code-block:: python

    @logger.decorate('This is a message.')
    def a():
        return 'This is a return'

Terminal output:

.. code-block:: bash

    2018-05-25 11:39:21,663 - Name - INFO - Connection to logstash successful.
    2018-05-25 11:39:21,669 - Name - DEBUG - This is a message

Logstash output:

.. code-block:: bash







