import os
from flask import Flask , render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import json 
import urllib2
import stripe
from config import *
from wallgen import *





stripe_keys = {
    'secret_key': SECRET_KEY,
    'publishable_key': PUBLISHABLE_KEY
}


stripe.api_key = stripe_keys['secret_key']



import sqlite3
from flask import g







app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
from config import *

from models import *

urlData = "https://blockchain.info/address/1QJ273C1Ry1yQxECTzoEHchLJS3Kqs9xM1?format=json"




def jSonstrip(web_url):
	weburl = urllib2.urlopen(web_url)
	if weburl.getcode() == 200:
		data = weburl.read()
		theJson = json.loads(data)
		return theJson
	else: return None 






@app.route('/')
def index():
	blockchain_data = jSonstrip(urlData)
    

	coin = blockchain_data["final_balance"]/100000000.0000
	return render_template('index.html', coin=coin, key=stripe_keys['publishable_key'])



@app.route('/contact/', methods=['POST'])
def contact():

    if methods == POST:

        email = request.form['email']
        message = request.form['message']

        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(gmail_user, gmail_pwd)
        header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
        print header
        msg = header + '\n this is test msg from mkyong.com \n\n'
        smtpserver.sendmail(gmail_user, to, msg)
        print 'done!'
        smtpserver.close()
        return " thank you an email has been sent to %s "   % email
    else: return render_template('contact.html')



@app.route('/subscribe')
def subscribe():
	return render_template('subscribe-form.html')





@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500


    stripe_token = request.form['stripeToken']
    email = request.form['stripeEmail']

    try:
        charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                card=stripe_token,
                description=email)
    except stripe.CardError, e:
        return """<html><body><h1>Card Declined</h1><p>Your chard could not
        be charged. Please check the number and/or contact your credit card
        company.</p></body></html>"""
    print charge

    pre_key = os.urandom(32).encode('hex')
    
    private_key = privateKeyToWif(pre_key)

    vals = Purchase(email=email, confirmed=stripe_token)
        
    db.session.add(vals)
    db.session.commit()



    message = 'Fuck you chelios'
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
    msg = header + '\n thank you for using lottabitz, this is your private key %s \n\n'  % private_key
    print header
    smtpserver.sendmail(gmail_user, email, msg)


    return render_template('charge.html', amount=amount, address=private_key)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500





@app.route('/thanks')
def thanks():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)
