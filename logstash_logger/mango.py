from logstash_logger import LogstashLogger

test = LogstashLogger("hehe")
#test.info("boi")





@test.decorator
def fallout():
    import time
    time.sleep(2)
    print("boi")

fallout()
