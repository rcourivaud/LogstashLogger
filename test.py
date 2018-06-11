from magic_logger import MagicLogger

logger = MagicLogger("random", host="localhost")

@logger.decorate()
def a(*args, **kwargs):
    import time
    time.sleep(2)
    return "hehehe"

a()
