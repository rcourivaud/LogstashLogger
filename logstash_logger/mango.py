from logstash_logger import LogstashLogger

test = LogstashLogger("oysta", extra={"radical":"cat", "depressing":"dear"})
#test.info("boi")

@test.decorate
def fallout():
    import time
    time.sleep(3)
    print("boi")

fallout()
