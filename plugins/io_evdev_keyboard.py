from .io_base import IOBase
import evdev
from select import select
import logging
import RPi.GPIO as GPIO
import time
logger = logging.getLogger(__name__)

        

class Plugin(IOBase):
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

    goal_map = {
        'KEY_KP4': 'yellow',  # KP_4
        'KEY_KP6': 'black',  # KP_6

        'KEY_A': 'yellow',  # A
        'KEY_D': 'black',  # D
    }

    def __init__(self, bus):
        self.devices = self.list_devices()
        buttonPin17 = 17
        buttonPin4 = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buttonPin17,GPIO.IN)
        GPIO.setup(buttonPin4, GPIO.IN)
        GPIO.add_event_detect(buttonPin4, GPIO.RISING, callback=self.button_press_callback, bouncetime=200)
        GPIO.add_event_detect(buttonPin17, GPIO.RISING, callback=self.button_press_callback, bouncetime=200)

        if len(self.devices) == 0:
            logger.warn("Can't find any keyboards to read from - maybe you need permissions")
        else:
            logger.info("Reading key events from: {}".format(self.devices))

        super().__init__(bus)
        
    def button_press_callback(self, channel):
        print ("got callback from channel: " + str(channel)) 
        state17 = GPIO.input(17)
        state4 = GPIO.input(4)
        print ("State17: " + str(state17) + " State 4: " + str(state4))
        if (channel == 4 and state17) or (channel == 17 and state4):
            print ("Both buttons are pushed")
        elif channel == 17:
#             if self.is_long_click(17):
#                 print("Black undo goal")
#                 self.simulate_click('KEY_Z')                
#             else:
            print("Black goal")
            self.simulate_click('KEY_Q')                
        elif channel == 4:
#             if self.is_long_click(4):
#                 print("Yellow undo goal")
#                 self.simulate_click('KEY_C')
#             else:
            print("Yellow goal")
            self.simulate_click('KEY_E')

    def is_long_click(self, channel):
        if GPIO.input(channel):
            time.sleep(0.5)
        return GPIO.input(channel)
        
    def simulate_click(self, key):
        self.handle_key(key, evdev.events.KeyEvent.key_down)
        time.sleep(0.05)
        self.handle_key(key, evdev.events.KeyEvent.key_up)
    
            
    def list_devices(self):
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        def hasAKey(device):
            caps = device.capabilities(verbose=True)
            events = caps.get(('EV_KEY', 1), [])
            a_keys = [e for e in events if e[0] == 'KEY_A']
            return len(a_keys) > 0
        
        return list(filter(hasAKey, devices))


    def handle_key(self, code, keystate):
        if keystate == evdev.events.KeyEvent.key_hold:
            return
        
        state = "down" if keystate == evdev.events.KeyEvent.key_down else "up"
        
        if code in self.key_map:
            btn = self.key_map[code]

            event_data = {'source': 'keyboard', 'btn': btn, 'state': state}
            print(event_data)
            self.bus.notify('button_event', event_data)

        if code in self.goal_map and state == "down":
            team = self.goal_map[code]
            self.bus.notify('goal_event', {'source': 'keyboard', 'team': team})
            
        if code == 'KEY_DOT':  # PERIOD
            self.bus.notify('quit')

    def reader_thread(self):
        # A mapping of file descriptors (integers) to InputDevice instances.
        devices = {dev.fd: dev for dev in self.devices}

        while True:
            r, w, x = select(devices, [], [])
            for fd in r:
                for event in devices[fd].read():
                    ce = evdev.categorize(event)
                    if isinstance(ce, evdev.KeyEvent):
                        self.handle_key(ce.keycode, ce.keystate)

        return

    def isStateChanged(self, input):
        print(input)
        print(self.prev_input)
        return input != self.prev_input
    
    def writer_thread(self):
        while True:
            self.write_queue.get()
            pass

