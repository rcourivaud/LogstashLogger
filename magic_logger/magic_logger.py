"""Main module."""
import sys
from logging import Logger, DEBUG, INFO, CRITICAL, ERROR, WARNING, raiseExceptions, FileHandler, StreamHandler, \
    Formatter, _checkLevel, addLevelName

from datetime import datetime
from logstash import TCPLogstashHandler

import os

import socket
import inspect

_srcfile = os.path.normcase(addLevelName.__code__.co_filename)


class MagicLogger(Logger):
    def __init__(self, logger_name,
                 file_name=None,
                 host="logstash",
                 port=5000,
                 extra=None,
                 blacklist=['self'],
                 **kwargs):
        """
        :param logger_name:
        :param file_name:
        :param host:
        :param port:
        :param extra:
        :param kwargs:
        """

        super().__init__(name=logger_name)

        self.extra = extra

        self.blacklist = [] if blacklist is None else blacklist

        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if file_name is not None:
            file_handler = FileHandler(filename=file_name)
            file_handler.setLevel(DEBUG)
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)

        # console logging
        console_handler = StreamHandler()
        console_handler.setLevel(DEBUG)
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

        # check for logstash connection success
        if host is not None:
            try:
                socket.socket().connect((host, port))
                self.info("Connection to logstash successful.")
                self.logstash_handler = TCPLogstashHandler(host, port, version=1)
            except (ConnectionRefusedError, socket.gaierror):
                self.log(level=ERROR, msg="Connection to logstash unsuccessful. ({0}:{1})".format(host, port))

    def decorate(self, msg=None, logstash=False, level=DEBUG, display_result=None, display_kwargs=None):
        msg_decorate = msg
        def _(f):
            def wrapper(*args, **kwargs):
                before = datetime.now()
                res = f(*args, **kwargs)
                after = datetime.now()
                execution_time = (after - before).total_seconds()

                kwargs = {
                    **kwargs,
                    **{arg_name: arg_value for arg_name, arg_value in zip(inspect.getfullargspec(f).args, args)}
                }

                if isinstance(res, list):
                    function_res = [str(res_elt) for res_elt in res]
                elif isinstance(res, dict):
                    function_res = {k: str(v) for k, v in res.items()}
                else:
                    function_res = str(res)

                extra_decorate = {
                    'function_name': f.__name__,
                    'execution_time': execution_time,
                    'function_class': kwargs.get("self").__class__.__name__ if kwargs.get("self") else None,
                    'function_kwargs': {k: str(v) if not isinstance(v, list) else str(v) for k, v in kwargs.items() if
                                        k not in self.blacklist} if display_kwargs else None,
                    'function_res': function_res if display_result else None,
                    'class': kwargs.get('self')
                }

                extra_decorate = {k: v for k, v in extra_decorate.items() if v}

                nonlocal msg

                msg = f'{msg_decorate + " > " if msg_decorate is not None else ""}' \
                      f'{extra_decorate["function_class"] + " > " if extra_decorate.get("function_class") else ""}' \
                      f'{extra_decorate["function_name"] if extra_decorate.get("function_name") else ""}'

                self.log(level=level, msg=msg.format(**kwargs),
                         extra_decorate=extra_decorate, logstash=logstash)

                return res
            return wrapper
        return _

    def update_extra(self, **kwargs):
        self.extra = kwargs if self.extra is None else {**self.extra, **kwargs}
