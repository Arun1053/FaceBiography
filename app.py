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



@app.route('/register')
def register():
    title = 'Register for the test'
    return render_template('register.html', title=title)


@app.route('/form', methods=['POST', 'GET'])
def form():

    first_name = request.form['fst_name']
    last_name = request.form['lst_name']
    email = request.form['email_id']
    # new_first_name = Survey_db(first_name_db=first_name)
    # new_last_name = Survey_db(last_name_db=last_name)
    # new_email = Survey_db(email_db=email) 

    email_body = """<pre> 
    Congratulations and Thank you.
    Go to the page: <a href="https://423554042a28.ngrok.io">click here</a>
    Thanks,
    XYZ Team.
    </pre>"""


    message = MIMEText(email_body,'html')
    message['Subject'] = 'Link for the Survey'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("neosoft.training.02@gmail.com", "p@ssNeo002")
    server.sendmail("neosoft.training.02@gmail.com", email, message.as_string())

    if not first_name or not last_name or not email:
        error_statement = "All fields are required"
        return render_template('register.html', error_statement=error_statement,
                               first_name=first_name,
                               last_name=last_name,
                               email=email)

    takers.append(f'{first_name} {last_name} | {email}')
    title = 'Thank you!'

    return render_template('form.html', title=title, takers=takers)



app.run(debug=True)
