from .io_base import IOBase
import RPi.GPIO as GPIO
import time
import logging

from foos.config import btn_pin_a
from foos.config import btn_pin_b
from foos.config import btn_min_duration
from foos.config import btn_sleep_time
from foos.config import btn_long_duration

logger = logging.getLogger(__name__)

# gpio state constants
NONE = (0, 0)
A_ONLY = (0, 1)
B_ONLY = (1, 0)
BOTH = (1, 1)

class Plugin(IOBase):
    def __init__(self, bus):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(btn_pin_a, GPIO.IN)
        GPIO.setup(btn_pin_b, GPIO.IN)

        self.state = NONE
        self.temp_state = NONE
        self.last_temp_change_time = time.time()
        self.last_state_change_time = time.time()

        super(Plugin, self).__init__(bus)

    def _change_state(self, new_state, new_state_duration):
        state_change_time = time.time() - new_state_duration
        last_state_duration = state_change_time - self.last_state_change_time
        if new_state == NONE:
            logger.info(self.state + ', duration: ' + str(last_state_duration))
            if self.state == BOTH:
                self.bus.notify('reset_score', {})
            else:
                team = 'black' if self.state == B_ONLY else 'yellow'
                operation = 'increment_score' if (last_state_duration < btn_long_duration) else 'decrement_score'
                self.bus.notify(operation, {'team': team})
        self.state = new_state
        self.last_state_change_time = state_change_time

    def reader_thread(self):
        while True:
            new_state = (GPIO.input(btn_pin_b), GPIO.input(btn_pin_a))
            if self.state == new_state:
                self.temp_state = self.state
            else:
                if self.temp_state == self.state or self.temp_state != new_state:
                    # first cycle for this change. let's see if it's long enough to count...
                    self.temp_state = new_state
                    self.last_temp_change_time = time.time()
                elif self.temp_state == new_state:
                    # we have been in the temp state already, let's check if we can call it a state change
                    temp_duration = time.time() - self.last_temp_change_time
                    if temp_duration >= btn_min_duration:
                        # State change!!!
                        self._change_state(new_state, temp_duration)
            time.sleep(btn_sleep_time)

    def writer_thread(self):
        while True:
            self.write_queue.get()
            pass
