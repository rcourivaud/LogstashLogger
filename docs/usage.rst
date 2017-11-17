=====
Usage
=====

To use Logstash Logger in a project::

    from logstash_logger import LogstashLogger

You just have to inherit from LogstashLogger Class::

    class MyClass(LogstashLogger):
        def __init__(self):
            super().__init__()
            pass

