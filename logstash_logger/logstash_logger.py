"""Main module."""
from logging import Logger, DEBUG, INFO, CRITICAL, ERROR, WARNING, raiseExceptions, FileHandler, StreamHandler, Formatter, _checkLevel

from logstash import TCPLogstashHandler

import os

import socket
import inspect


class LogstashLogger(Logger):
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

        if file_name is not None: self.addHandler(FileHandler(filename=file_name))

        self.addHandler(TCPLogstashHandler(host, port, version=1))

        #console logging
        console_handler = StreamHandler()
        console_handler.setLevel(DEBUG)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

        #console logging checking for logstash connection success
        try:
            socket.socket().connect((host, port))
            self.info("Connection to logstash successful.")
        except (ConnectionRefusedError, socket.gaierror):
            self.log(level=ERROR, msg="Connection to logstash unsuccessful. ({0}:{1})".format(host, port))

    def decorate(self, msg="Example message", level=DEBUG):
        if isinstance(level, str): level = level.upper()
        def _(f):
            def wrapper(*args,**kwargs):
                import datetime
                before = datetime.datetime.now()
                res = f(*args,**kwargs)
                after = datetime.datetime.now()
                execution_time = (after-before).total_seconds()

                kwargs = {
                        **kwargs,
                        **{arg_name:arg_value for arg_name, arg_value in zip(inspect.getfullargspec(f).args, args)}
                        }

                extra = {
                        "function_name": f.__name__,
                        "execution_time": execution_time,
                        "function_class": kwargs.get("self").__class__.__name__ if kwargs.get("self") else None,
                        }
                extra = {
                        **extra,
                        **{'function_kwargs': {k:str(v) for k, v in kwargs.items() if k not in self.blacklist},
                            'function_res': res,
                            'class': kwargs.get('self')}}

                self.log(level=_checkLevel(level), msg=msg.format(**kwargs), extra_decorate=extra)

                return res
            return wrapper
        return _

    def log(self, level, msg, extra_decorate=None, *args, **kwargs):
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", "mysterious problem", exc_info=1)
        """

        extra_temp = {}

        if self.extra is not None: extra_temp.update(self.extra)
        if extra_decorate is not None: extra_temp.update(extra_decorate)

        kwargs["extra"] = extra_temp

        if not isinstance(level, int):
            if raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return
        if self.isEnabledFor(level):
            self._log(level, msg, args, **kwargs)
