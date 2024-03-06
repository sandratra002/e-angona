from models.church import Church
from models.believer import Believer
from utils.utils import get_sunday_id_int as ids, get_sunday_date
import datetime as dt
from datetime import datetime
from models.auth import Authentication
from flask import Flask, render_template

app = Flask(__name__, static_folder = "assets")

@app.route('/')
def index():
    return "Hello World"

@app.route('/login-forom')
def login_form():
    return render_template("")
    
app.run()