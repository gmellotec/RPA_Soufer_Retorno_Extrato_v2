from custom_logging import Log
from custom_path import CustomPath
from config import ConfigLoader
from botcity.core import DesktopBot

_dirs = [
    "apps",
    "config",
    "data",
    "data/input",
    "data/output",
    "data/images",
    "data/downloads",
    "templates",
    "templates/database",
    "templates/email",
    "log",
    "stages",
    "tests",
    "utils",
    "workflow"
]

path = CustomPath(_dirs)
log = Log()
config = ConfigLoader()
bot = DesktopBot()


__all__ = [
    'log',
    'config',
    'path',
    'bot'
]