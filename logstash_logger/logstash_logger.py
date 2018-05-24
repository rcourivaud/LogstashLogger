"""Main module."""
import sys
from logging import Logger, DEBUG, INFO, CRITICAL, ERROR, WARNING, raiseExceptions, FileHandler, StreamHandler, \
    Formatter, _checkLevel, addLevelName

from logstash import TCPLogstashHandler

import os

import socket
import inspect

_srcfile = os.path.normcase(addLevelName.__code__.co_filename)


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
                        **{
                            'function_kwargs': {k:str(v) for k, v in kwargs.items() if k not in self.blacklist},
                            'function_res': res,
                            'class': kwargs.get('self')
                        }
                }

                self.log(level=level, msg=msg.format(**kwargs), extra_=extra)

                return res
            return wrapper
        return _

    def log(self, level, msg, extra_=None, *args, **kwargs):
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", "mysterious problem", exc_info=1)
        """

        if self.isEnabledFor(_checkLevel(level)):
            self._log(_checkLevel(level), msg, args, **kwargs)

    def _log(self, level, msg, args, exc_info=None, extra=None, extra_=None, stack_info=False):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        level = _checkLevel(level.upper()) if isinstance(level, str) else level

        extra = {**(extra if extra else {}) , **(extra_ if extra_ else {}), **(self.extra if self.extra else {})}

        sinfo = None
        if _srcfile:
            # IronPython doesn't track Python frames, so findCaller raises an
            # exception on some versions of IronPython. We trap it here so that
            # IronPython can use logging.
            try:
                fn, lno, func, sinfo = self.findCaller(stack_info)
            except ValueError:  # pragma: no cover
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:  # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, fn, lno, msg, args,
                                 exc_info, func, extra, sinfo)
        self.handle(record)

    def update_extra(self, **kwargs):
        self.extra = kwargs if self.extra is None else {**self.extra, **kwargs}
