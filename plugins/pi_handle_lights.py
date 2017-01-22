from .io_base import IOBase
import RPi.GPIO as GPIO
import time
import logging
from time import sleep
from threading import Thread

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
        if ev.name == "increment_score":
            Thread(target=self.blink_light(ev.data['team'])).start()

    def blink_light(self, team):
        blink_team = yellow_team_light if team=='yellow' else black_team_light
        for i in range(4): 
           GPIO.output(blink_team, GPIO.HIGH)
           sleep(0.2)
           GPIO.output(blink_team, GPIO.LOW)
           sleep(0.2)
