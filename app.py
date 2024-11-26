from flask import Flask, render_template, flash, request, session,send_file
from flask import render_template, redirect, url_for, request
import mysql.connector
import sys

import pickle


import numpy as np

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1airqualitydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()
    return render_template('AdminHome.html',data=data)


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')

@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['pas'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1airqualitydb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("You Are Logged In....!")
            return render_template('AdminHome.html', data=data)

        else:
            flash("Username or Password is wrong")
            return render_template('AdminLogin.html')

@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')

@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        city = request.form['city']
        address = request.form['address']
        uname = request.form['uname']
        pas = request.form['pas']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1airqualitydb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into regtb values('','" + name + "','" + email + "','" + mobile + "','" + city + "','" + address + "','" + uname + "','" + pas + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")

    return render_template('NewUser.html')

@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():

    if request.method == 'POST':
        uname = request.form['uname']
        pas = request.form['pas']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1airqualitydb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where Name='" + uname + "' and password='" + pas + "'")
        data = cursor.fetchone()
        if data is None:
            flash("UserName or Password is wrong...!")

            return render_template('UserLogin.html')

        else:
            session['email'] = data[2]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1airqualitydb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where Name='" + uname + "' and password='" + pas + "'")
            data = cur.fetchall()
            flash("Your are Logged In...!")

            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1airqualitydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where UserName='"+ uname +"'")
    data = cur.fetchall()
    return render_template('UserHome.html',data=data)

@app.route("/Predict")
def Predict():
    return render_template('Predict.html')


@app.route("/result", methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        email = session['email']
        t1 = request.form['t1']
        t2 = request.form['t2']
        t22 = request.form['t22']
        t23 = request.form['t23']
        t24 = request.form['t24']
        t25 = request.form['t25']
        t26 = request.form['t26']
        t27 = request.form['t27']
        t28 = request.form['t28']




        filename = 'prediction-rfc-model.pkl'
        classifier = pickle.load(open(filename, 'rb'))

        data = np.array([[t1,t2, t22, t23, t24,t25, t26,t27,t28 ]])

        my_prediction = classifier.predict(data)


        print(my_prediction[0])
        Answer = ''

        tre = ''

        if my_prediction == 0:
            Answer = 'Good'
            color = 'green'

        elif my_prediction == 1:
            Answer = 'Moderate'
            color = 'pink'
        elif my_prediction == 2:
            Answer = 'Unhealthy'
            color = 'orange'
        elif my_prediction == 3:
            Answer = 'very_unhealthy'
            color = 'red'
        sendmail(email,"Air Quality "+str(Answer))


        return render_template('Predict.html', res=Answer,color=color)






def sendmail(Mailid,message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)