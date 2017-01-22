from .io_base import IOBase
import RPi.GPIO as GPIO
import time
import logging

from foos.config import black_team_light, yellow_team_light

logger = logging.getLogger(__name__)

class Plugin(IOBase):
    def __init__(self, bus):
        GPIO.setmode(GPIO.BCM)
        for light_plug in [yellow_team_light, black_team_light]:
            GPIO.setup(light_plug, GPIO.OUT)
            # lights out at init
            GPIO.output(light_plug, GPIO.LOW)
        self.bus = bus
        self.bus.subscribe(self.process_event, thread=True)
        super(Plugin, self).__init__(bus)

    def process_event(self, ev):
        logger.info("I'm in process events !!! " + str(ev))

