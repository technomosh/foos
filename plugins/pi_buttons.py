from .io_base import IOBase
import RPi.GPIO as GPIO
import time
import logging
logger = logging.getLogger(__name__)

# module constants
# adjust for where your switch is connected
# TODO: populate this from the config
buttonPin17 = 17
buttonPin4 = 4
NONE = (0, 0)
A_ONLY = (0, 1)
B_ONLY = (1, 0)
BOTH = (1, 1)
event_names = {NONE: 'NONE', A_ONLY: 'A', B_ONLY: 'B', BOTH: 'BOTH'}
team_names = {A_ONLY: 'yellow', B_ONLY: 'black'}

MIN_DURATION = 0.05
#sleep needs to be <= min_duration
SLEEP_TIME = 0.05

key_map = {
    'KEY_KP1': 'yellow_minus',  # KP_1
    'KEY_KP7': 'yellow_plus',  # KP_7
    'KEY_KP3': 'black_minus',  # KP_3
    'KEY_KP9': 'black_plus',  # KP_9
    'KEY_KP5': 'ok',  # KP_5

    'KEY_Q': 'yellow_plus',  # Q
    'KEY_E': 'black_plus',  # E
    'KEY_S': 'ok',  # S
    'KEY_Z': 'yellow_minus',  # Z
    'KEY_C': 'black_minus',  # C
}


class Plugin(IOBase):
    def __init__(self, bus):
        self.bus = bus
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buttonPin17, GPIO.IN)
        GPIO.setup(buttonPin4, GPIO.IN)
        self.state = NONE
        self.temp_state = NONE
        self.last_temp_change_time = time.time()
        self.last_state_change_time = time.time()
        super(Plugin, self).__init__(self.bus)

    def _change_state(self, orig_state, new_state, new_state_duration):
        state_change_time = time.time() - new_state_duration
        last_state_duration = state_change_time - self.last_state_change_time
        if new_state == NONE:
            logger.info(event_names[self.state] + ', duration: ' + str(last_state_duration))
            event_data = {'source': 'keyboard', 'team': team_names[orig_state]}
            self.bus.notify('goal_event', event_data)

        self.state = new_state
        self.last_state_change_time = state_change_time

    def reader_thread(self):
        while True:
            new_state = (GPIO.input(buttonPin4), GPIO.input(buttonPin17))

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
                    if temp_duration >= MIN_DURATION:
                        # State change!!!
                        self._change_state(self.state, new_state, temp_duration)
            time.sleep(SLEEP_TIME)

    def writer_thread(self):
        while True:
            self.write_queue.get()
            pass
