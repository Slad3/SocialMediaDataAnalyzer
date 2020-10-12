import os
from waitress import serve

from App import app

serve(app, port=8091)