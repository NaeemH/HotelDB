from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
#from databases import * #imports all the DBs from databases.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "GENERIC PASSWORD"

db = SQLAlchemy(app)
request
def __init__(self, name, username, password):
	self.name = name
	self.username = username
	self.password = password

#------------------------- DATABASE DEFINITIONS ------------------------
class usersDB(db.Model):
	id = db.Column('uid', db.Integer, primary_key=True, nullable=False)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(120), nullable=False)

class creditCardDB(db.Model):
	id = db.Column('customerID', db.Integer, primary_key=True, nullable=False, autoincrement=True)
	cnumber = db.Column(db.String(16), nullable = False)
	name = db.Column(db.String(20), nullable = False)
	billingAddr = db.Column(db.String(30), nullable=False)
	secCode = db.Column(db.Integer, nullable = False)
	cardType = db.Column(db.String(10), nullable = False)
	expirationMonth = db.Column(db.Integer, nullable=False)
	expirationYear = db.Column(db.Integer, nullable=False)

class homeAddressDB(db.Model):
	id = db.Column('uid', db.Integer, primary_key=True, nullable=False)
	street = db.Column(db.String(30), nullable = False)
	state = db.Column(db.String(2), nullable = False)
	zipCode = db.Column(db.Integer, nullable=False)
	country = db.Column(db.String(3), nullable=False)

class billingAddressDB(db.Model):
	id = db.Column('customerID', db.Integer, primary_key=True, nullable=False)
	street = db.Column(db.String(20), nullable = False)
	city = db.Column(db.String(10), nullable = False)
	state = db.Column(db.String(2), nullable = False)
	zipCode = db.Column(db.Integer, nullable = False)

class expirationDateDB(db.Model):
	id = db.Column('customerID', db.Integer, primary_key=True, nullable=False)
	month = db.Column(db.Integer, nullable=False)
	year = db.Column(db.Integer, nullable=False)

class breakfastReviewDB(db.Model):
	id = db.Column('customerID', db.Integer, primary_key=True, nullable=False)
	textComment = db.Column(db.String(200))

class roomReviewDB(db.Model):
	id = db.Column('customerID', db.Integer, primary_key=True, nullable=False)
	textComment = db.Column(db.String(200))

class serviceReviewDB(db.Model):
	id = db.Column('customerID', db.Integer, primary_key=True, nullable=False)
	textComment = db.Column(db.String(200))

class reservationDB(db.Model):
	id = db.Column('customerID', db.Integer, primary_key=True, nullable=False)
	location = db.Column(db.String(12), nullable=False)
	startDate = db.Column(db.String(10), nullable=False)
	endDate = db.Column(db.String(10), nullable=False)
	party = db.Column(db.Integer, nullable=False)
	breakfast = db.Column(db.Integer, nullable=False)
	room = db.Column(db.Integer, nullable=False)
	payperview = db.Column(db.Integer, nullable=False)
	bedType = db.Column(db.Integer, nullable=False)
	special = db.Column(db.String(100))
	
# --------------------------------------------------------------------------

@app.route('/', methods = ['GET', 'POST']) #equivalent to index.html
def login(): 
	if request.method == 'GET':
		return render_template('login.html')
	if request.method == 'POST':
		check_username = request.form.get('username')
		check_password = request.form.get('password')
		if request.form.get("draft") == 'Register': #register
			flash("Registered User with username="+check_username+", password="+check_password+"\n")
			user = usersDB(username=check_username, password=check_password)
			checkUsername = usersDB.query.filter_by(username=request.form.get('username')).first()

			if checkUsername is not None:
				flash("Username already exists!")
				return render_template('login.html')
			else:
				db.session.add(user)
				db.session.commit()
				flash("Registration successful!")
				return render_template('login.html')
			
		else: #login
			if request.form.get("username") == 'username':
				if request.form.get("password") == 'password':
					return redirect(url_for('stats'))
			
			flash("trying to log in with username="+request.form.get("username")+", password="+request.form.get("password")+". ")
			validateUser = usersDB.query.filter_by(username=request.form.get('username'),password=request.form.get('password')).first()
			if validateUser is None:				
				flash("Invalid credentials.")
				return render_template('login.html')
			else:
				return redirect(url_for('home'))
	return render_template(('login.html'))

@app.route('/stats', methods = ['GET', 'POST']) #stats for nerds page - see the DB!
def stats():
	 #removes everything from the DB
	if request.form.get("dbmanipulation") == "Purge DB":
		db.session.query(usersDB).delete()
		db.session.query(creditCardDB).delete()
		db.session.query(homeAddressDB).delete()
		db.session.query(expirationDateDB).delete()
		db.session.query(creditCardDB).delete()
		db.session.query(billingAddressDB).delete()
		db.session.query(reservationDB).delete()
		db.session.query(breakfastReviewDB).delete()
		db.session.query(roomReviewDB).delete()
		db.session.query(serviceReviewDB).delete()
		db.session.commit()
	 #does the actual querying
	return render_template('show_all.html', showUsers = usersDB.query.all(), showCredits = creditCardDB.query.all(), showHomeAddresses = homeAddressDB.query.all(), showBillingAddresses = billingAddressDB.query.all(), showExpirationDates = expirationDateDB.query.all(), showCreditCards = creditCardDB.query.all(), showReservations=reservationDB.query.all(), showBreakfastReviews = breakfastReviewDB.query.all(), showRoomReviews = roomReviewDB.query.all(), showServiceReviews = serviceReviewDB.query.all() )

@app.route('/home', methods = ['GET', 'POST']) #home page - what the user first sees the moment they log in.
def home():
	if request.form.get('draft') == 'Make a Reservation':
		return redirect(url_for('reservations'))
	elif request.form.get('draft') == 'View/Alter your Reservation':
		return redirect(url_for('showreservation'))
	elif request.form.get('draft') == 'Write a review':
		return redirect(url_for('review'))
	return render_template('home.html')

@app.route('/reservations', methods = ['GET', 'POST']) #site for storing customer information / reservation
def reservations():
	if request.method == 'GET':	
		return render_template('reservations.html', showReservations = reservationDB.query.all())
	if request.method == 'POST':	
		location = request.form.get("location")
		name = request.form.get("name")
		email = request.form.get("email")
		phone = request.form.get("phone")
		street = request.form.get("street")
		state = request.form.get("state")
		zipCode = request.form.get("zip")
		country = request.form.get("country")
		checkInDate = request.form.get("arrive")
		checkOutDate = request.form.get("depart")
		numPeople = request.form.get("numPersons")
		breakfastService = 0 #false
		roomService = 0 #false
		payService = 0 #false
		bedType = request.form.get("numBeds")
		specialRequests = request.form.get("comments")
		if request.form.get("breakfastfeature"):
			breakfastService = 1 #true
		if request.form.get("roomfeature"):
			roomService = 1
		if request.form.get("servicefeature"):
			payService = 1	
		# commits stuff to home address DB.
		if request.form.get("draft") == 'Continue':
			reservation = reservationDB(location=location, startDate=checkInDate, endDate=checkOutDate, party=numPeople, breakfast=breakfastService, room=roomService, payperview=payService, bedType=bedType, special=specialRequests)
			home = homeAddressDB(street=street, state=state, zipCode=zipCode, country=country)
			db.session.add(home)
			db.session.add(reservation)
			db.session.commit()
			return redirect(url_for('cardform'))
	return render_template('reservations.html')


@app.route('/showreservation', methods = ['GET', 'POST']) #shows current available reservations.
def showreservation():
	if request.method == 'GET':
		return render_template('showReservation.html', showReservations=reservationDB.query.all())
	if request.method == 'POST':
		flash('Reservations updated!')
		return redirect(url_for('home'))
	return render_template('showReservation.html')

@app.route('/review', methods = ['GET', 'POST']) #submits written reviews to DB.
def review():
	if request.method == 'GET':
		return render_template('review.html')
	if request.method == 'POST':
		breakfastText = request.form.get("breakfasttext")
		roomText = request.form.get("roomtext")
		serviceText = request.form.get("servicetext")
		breakfastReview = breakfastReviewDB(textComment=breakfastText)
		roomReview = roomReviewDB(textComment=roomText)
		serviceReview = serviceReviewDB(textComment=serviceText)
		db.session.add(breakfastReview)
		db.session.add(roomReview)
		db.session.add(serviceReview)			
		db.session.commit()			
		return redirect(url_for('home'))
	
	return render_template('review.html')

@app.route('/cardform', methods = ['GET', 'POST']) #site for storing card information.
def cardform():
	if request.method == 'GET':
		return render_template('cardForm.html')
	if request.method == 'POST':	
		name = request.form.get("name-card")
		street = request.form.get("street-card")
		city = request.form.get("city-card")
		state = request.form.get("state-card")
		zipCode = request.form.get("zip-card")
		cardNumber = request.form.get("number-card")
		cardType = request.form.get("type-card")
		validMonth = request.form.get("mm-card")
		validYear = request.form.get("year-card")
		cvv = request.form.get("cvc-card")
		
		if request.form.get("submitData") == 'Confirm':
			expirationDate = expirationDateDB(month=validMonth, year=validYear)
			billingAddress = billingAddressDB(street=street, city=city, state=state, zipCode=zipCode)
			creditCard = creditCardDB(cnumber=cardNumber, name=name, billingAddr=street, secCode=cvv, cardType=cardType, expirationMonth=validMonth, expirationYear=validYear)
			db.session.add(billingAddress)
			db.session.add(expirationDate)
			db.session.add(creditCard)
			db.session.commit()	
			return redirect(url_for('home'))
		
	return render_template('cardForm.html')


# sets up the address of the site

if __name__ == '__main__':
	db.create_all()	
	app.run(port=5000, host='localhost', debug=True)
