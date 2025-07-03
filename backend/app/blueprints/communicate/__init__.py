from flask import Blueprint

communicate_bp = Blueprint("communicate", __name__)

from .chatbot_utils import *
from .chatbot import *
from .parking import *
from .height import *