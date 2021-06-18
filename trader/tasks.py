from daytrader import tasker
import time

@tasker.task(bind=True)
def wait_10(self):
    time.sleep(10)

