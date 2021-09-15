from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient

app = Flask(__name__)

takers = []


@app.route('/')
def index():
    return render_template('index.html')

z`

@app.route('/register')
def register():
    title = 'Register for the test'
    return render_template('register.html', title=title)

@app.route('/quest')
def quest():
    title = 'Take the survey'
    return render_template('survey_Q.html', title=title)

@app.route('/form', methods=['POST'])
def form():

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    age = request.form.get('age')
    marital_status = request.form.get('marital_status')
    gender = request.form.get('gender')
    contact = request.form.get('contact')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zipcode = request.form.get('zipcode')

    email_body = """<pre> 
    Congratulations and Thank you.
    Go to the page: <a href="http://58f9-1-186-179-2.ngrok.io">click here</a>
    Thanks,
    XYZ Team.
    </pre>"""


    message = MIMEText(email_body,'html')
    message['Subject'] = 'Link for the Survey'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("neosoft.training.02@gmail.com", "p@ssNeo002")
    server.sendmail("neosoft.training.02@gmail.com", email, message.as_string())

    if not first_name or not last_name or not email or not age or not marital_status or not gender or not address or not city or not state or not zipcode or not contact:
        error_statement = "All fields are required"
        return render_template('register.html', error_statement=error_statement,
                               first_name=first_name,
                               last_name=last_name,
                               email=email,
                               age=age,
                               marital_status=marital_status,
                               gender=gender,
                               address=address,
                               city=city,
                               state=state,
                               zipcode=zipcode)

    takers.append(f'{first_name} {last_name} | {email}')
    title = 'Thank you!'

    return render_template('form.html', title=title, takers=takers)



app.run(debug=True)
