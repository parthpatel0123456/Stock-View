import sys
print(sys.executable)

from flask import Flask

def create_app():
    app = Flask(__name__)