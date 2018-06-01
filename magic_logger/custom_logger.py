import sys
from logging import Logger, DEBUG, INFO, CRITICAL, ERROR, WARNING, _checkLevel, addLevelName

import os

_srcfile = os.path.normcase(addLevelName.__code__.co_filename)

class CustomLogger(Logger):


    def debug(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        if self.isEnabledFor(DEBUG):
            return self._log(DEBUG, msg, args, **kwargs)



    def info(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if self.isEnabledFor(INFO):
            return self._log(INFO, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        if self.isEnabledFor(WARNING):
            return self._log(WARNING, msg, args, **kwargs)




    def error(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "major problem", exc_info=1)
        """
        if self.isEnabledFor(ERROR):
            return self._log(ERROR, msg, args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
        Convenience method for logging an ERROR with exception information.
        """
        return self.error(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        if self.isEnabledFor(CRITICAL):
            return self._log(CRITICAL, msg, args, **kwargs)

    fatal = critical


    def log(self, level, msg, extra_decorate=None, *args, **kwargs):
        """
        Log 'msg % args' with the integer severity 'level'.
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        logger.log(level, "We have a %s", "mysterious problem", exc_info=1)
        """

        #extra_decorate = {**(extra_decorate if extra_decorate else {})}

        if self.isEnabledFor(_checkLevel(level)):
            self._log(_checkLevel(level), msg, args, **kwargs, extra_decorate=extra_decorate)


    def _log(self, level, msg, args, exc_info=None, extra=None, extra_decorate=None, stack_info=False):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        level = _checkLevel(level.upper()) if isinstance(level, str) else level

        extra = {**(extra if extra else {}) , **(extra_decorate if extra_decorate else {}), **(self.extra if self.extra else {})}

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
        return record

