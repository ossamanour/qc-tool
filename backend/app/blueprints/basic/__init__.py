from flask import Blueprint

basic_bp = Blueprint("basic", __name__)

from .auth import *
from .image import *
from .load import *
from .task import *
from .pricesheet import *