from flask import Blueprint
from index import *
app_views = Blueprint('simple_page', url_prefix='/api/v1')
