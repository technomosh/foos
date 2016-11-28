""" Override config values from config_base using this file """
from foos.config_base import *


""" Configure the plugin set """

# -- Enable camera, replays and video motiondetector
#plugins.update(set(['replay', 'camera', 'motiondetector']))

# -- Modify this to tune your camera settings - see raspivid --help for more info
#camera_extra_params = "--ev 7"

# -- Enable league sync with server
#plugins.add('league_sync')

# -- Enable Youtube video upload
#plugins.add('upload')

# -- Enable hipchat bot
#plugins.add('hipbot')

# -- Enable Arduino serial input and led output
#plugins.add('io_serial')

# -- Enable auto-TV standby
plugins.add('standby')

# -- Enable pi buttons (GPIO)
#plugins.add('pi_buttons')

# -- Enable the old buttons version
plugins.add('io_evdev_keyboard')

""" Configure team names and colors """
#team_names = {"yellow": "blue", "black": "red"}
#team_colors = {"yellow": (0.1, 0.1, 0.4), "black": (0.7, 0, 0)}

""" Configure paths """

# -- replay path
#replay_path = "..."

# -- or the location of the file_handler
#log["handlers"]["file_handler"]["filename"] = ""


""" Override tokens for plugins """

#hipchat_token = 'your_token'
#hipchat_room = 'your_room_id'

#league_url = 'http://localhost:8888/api'
#league_apikey = 'put-your-apikey-here'
