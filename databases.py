from app import app, db # needed in order to use db.Model

#Just put the DBs like the following below! Be aware, however, that I used 'TAB' in lieu of spacing. It doesn't matter which is used, just keep it consistent throughout the file (lest you run into pesky 'invalid use of space/tab' errors).

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
	
