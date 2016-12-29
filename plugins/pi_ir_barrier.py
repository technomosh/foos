from .io_base import IOBase
import RPi.GPIO as GPIO
import time
import logging

from foos.config import ir_pin_a
from foos.config import ir_pin_b
from foos.config import ir_dedup_seconds

logger = logging.getLogger(__name__)


class Plugin(IOBase):
    def __init__(self, bus):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ir_pin_a, GPIO.IN)
        GPIO.setup(ir_pin_b, GPIO.IN)
        GPIO.add_event_detect(ir_pin_a, GPIO.RISING, callback=self.ir_callback, bouncetime=200)
        GPIO.add_event_detect(ir_pin_b, GPIO.RISING, callback=self.ir_callback, bouncetime=200)
        self.last_signal_time = 0;
        super(Plugin, self).__init__(bus)

    def ir_callback(self, channel):
        now = time.time()
        if now - self.last_signal_time > ir_dedup_seconds:
            logger.info('IR event on GPIO ' + str(channel))
            team = 'black' if channel == ir_pin_a else 'yellow'
            self.bus.notify('increment_score', {'team': team})
            self.last_signal_time = now
        else:
            logger.info('IR event dedupped on GPIO ' + str(channel))

    def reader_thread(self):
        while True:
            time.sleep(0.05)
            pass

    def writer_thread(self):
        while True:
            self.write_queue.get()
            pass
