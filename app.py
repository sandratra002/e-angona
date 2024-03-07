from decimal import Decimal
from models.church import Church
from models.donation import Donation
from models.believer import Believer
from models.loan import Loan

from utils.utils import get_sunday_id_int as ids, get_sunday_date, to_datetime

import datetime as dt
from datetime import datetime
from datetime import date

from models.auth import Authentication
from flask import Flask, render_template, request, redirect, session
import json
# from flask_session import Session

app = Flask(__name__, static_folder = "assets")
app.config['SECRET_KEY'] = 'aina'

@app.route('/')
def index():
    user = session.get("user")
    if( user ) :
        user = json.loads(user)
        return render_template("index.html", user = user)
    return render_template("index.html")
    # return user

@app.route('/login-form')
def login_form():
    error = session.get('error')
    if error :
        return render_template("login.html", error = error)
    else : 
        return render_template("login.html")
    
@app.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    password = request.form['password']
    believer = Authentication.login(id = id, pwd=password)
    if ( not believer) : 
        session['error'] = "An error has occurese"
        # return session['error']
        return redirect("/login-form")
    else :
        json_data = json.dumps(believer, default=lambda o: o.__dict__)
        session['user'] = json_data
        return redirect("/")

@app.route('/donation-form')
def donation_form():
    churches = Church().read()
    return render_template("donation.html", churches = churches)

@app.route('/donation', methods = ['POST'])
def donation():
    church_id = request.form['church_id']
    amount = float(request.form['amount'])
    date = request.form['date']
    sunday_id = ids(date=date)
    donation = Donation(church_id=church_id, amount=amount, date=date, sunday_id=sunday_id, is_prediction= 0)
    donation.create()
    return redirect("/")

@app.route('/prediction-form')
def prediction_form():
    return render_template("prediction-form.html")

@app.route('/prediction', methods = ['POST'])
def prediction():
    request_date = dt.datetime.strptime(to_datetime(request.form['request_date']), "%Y-%m-%d %H:%M:%S")
    print(request_date)
    amount = Decimal(request.form['amount'])
    user = session.get("user")
    user = json.loads(user)
    believer = Believer(id=user["id"])
    loan = believer.request_loan(date=request_date, amount=amount)
    church = Church(id=user["church_id"]).read_by_id()
    church.handle_loan_request(loan)
    print(loan.delivery_date)
    return str(loan.delivery_date)

@app.route('/donations')
def donations():
    donations = Donation().read()
    return render_template("donations.html", donations = donations)

@app.route('/loans')
def loans():
    loans = Loan().read()
    return render_template("predictions.html", loans = loans)
# app.run()
app.run(debug=True)
