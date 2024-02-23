from flask import Flask
import os
app = Flask(__name__)
header= os.environ.get("SESSION_KEY")
app.secret_key = header
