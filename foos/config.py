from foos.config_base import *
try:
    from config import *
except ImportError:
    pass
