from logstash_logger import LogstashLogger

test = LogstashLogger("example_logger_name", extra={"example_extra1": "boi", "example_extra2": "boo"})
#test = LogstashLogger("hunta")
#test.info("boi")

@test.decorate
def example_function(*args, **kwargs):
    import time
    time.sleep(1)
    return "example_return"

example_function("arg_1", "arg_2", arg_3="bah", arg_4="boh")
