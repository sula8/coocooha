from .config import DevConfig
from . import create_app


app = create_app(DevConfig)

