# Importing all needed Flask classes
from flask import Flask, jsonify, request, make_response, session

# Imporiting Flask Session Extention
# from flask.ext.session import Session

# Importing current user from flask
from flask_login import current_user

# Importing firebase connection through python
import pyrebase

# Importing JWT to encode and decode sensitive information
import jwt

# Importing os to encode session variable
import os

# Configuring connection to database
config = {
    'apiKey': "AIzaSyB-zW5qNKkTlfLzhbigIZkMWypJ4XMAAvY",
    'authDomain': "cpanel-8d88a.firebaseapp.com",
    'databaseURL': "https://cpanel-8d88a.firebaseio.com",
    'projectId': "cpanel-8d88a",
    'storageBucket': "cpanel-8d88a.appspot.com",
    'messagingSenderId': "955905061850"
  }

# Defining variable equal to database connection
firebase = pyrebase.initialize_app(config)

# Test Variables
database = firebase.database()

# Defing users with
authe = firebase.auth()

# Defing app which is nessisary for flask to run
app = Flask(__name__)

app.secret_key = os.urandom(24)

# Register Function
@app.route("/create-user", methods=['POST'])
def register():
	userData = dict()
	userReturn = []

	# Getting posted data and putting it in a dictionary
	userData['email'] = request.json['email']
	userData['password'] = request.json['password']

	# Assigning variables to sign in to database
	email = request.json['email']
	password = request.json['password']

	print(userData)
	try:
		# Attemptingto sign in to backend
		user = authe.create_user_with_email_and_password(email,password)

		# Assigning json data to variable to return to database
		userInstagramDefault = {"bio" : "0", "instagram_username" : "0", "number_of_followers" : 0, "number_of_following" : 0, "number_of_post" : 0, "on_desktop" : False, "on_mobile" : False, "on_web" : False}
		userTwitterDefault = {"bio" : "0", "twitter_username" : "0", "number_of_followers" : 0, "number_of_following" : 0, "number_of_post" : 0, "on_desktop" : False, "on_mobile" : False, "on_web" : False}
		
		# Assigning uid which will be used to create paths in database
		uid = user['localId']

		# Creating branches
		database.child("users").child(uid).child("details").child("instagram").set(userInstagramDefault)
		database.child("users").child(uid).child("details").child("twitter").set(userTwitterDefault)
	except Exception as e:
		print(e)
		userData['message'] = 'failed'
		return jsonify(userData)
	
	# Appending data into list ready to return
	userReturn.append(userData)
	userReturn.append(userInstagramDefault)
	userReturn.append(userTwitterDefault)
	
	print(userReturn)
	userData['message'] = 'success'

	return jsonify(userReturn)

# Signin Function
@app.route("/signin", methods=['POST'])
def signIn():
	userData = dict()

	# Creating list ready to return later
	userReturn = []

	# Assigning values to list for for loop to go though
	instagramItemList = ['bio', 'instagram_username', 'number_of_followers', 'number_of_following', 'number_of_post', 'on_desktop', 'on_mobile', 'on_web']
	twitterItemList = ['bio', 'twitter_username', 'number_of_followers', 'number_of_following', 'number_of_post', 'on_desktop', 'on_mobile', 'on_web']
	
	# Getting posted data and putting it in a dictionary
	userData['email'] = request.json['email']
	userData['password'] = request.json['password']

	# Assigning variables to sign in to database
	email = request.json['email']
	password = request.json['password']

	try:
		# Attemptingto sign in to backend
		user = authe.sign_in_with_email_and_password(email, password)

		# Assigning uid as a variable which will be used to go through branched in for loop
		uid = user['localId']

		# Creating dict to store data from database
		returnedInfoInstagram = dict()
		returnedInfoTwitter = dict()

		# For loops to gather information for each branch
		for i in instagramItemList:

			# Getting paths from database and assign to variable
			instagramItem = database.child("users").child(uid).child("details").child("instagram").child(i).get().val()
			returnedInfoInstagram[i] = instagramItem

		for i in twitterItemList:

			# Getting paths from database and assign to variable
			twitterItem = database.child("users").child(uid).child("details").child("twitter").child(i).get().val()
			returnedInfoTwitter[i] = twitterItem

	# If signin or gathering data fails will return failed
	except Exception as e:
		print(e)
		userData['message'] = 'failed'
		return jsonify(userData)

	# Saving success as message
	userData['message'] = 'success'

	# Appending data into list ready to return
	userReturn.append(userData)
	userReturn.append(returnedInfoInstagram)
	userReturn.append(returnedInfoTwitter)

	# Saving gathered data in session
	session['user'] = user
	session['data'] = userReturn
	# print(userReturn)
	print(userReturn)
	# Returning main data
	return jsonify(userReturn)

# Signout Function
@app.route("/signout", methods=['POST'])
def signOut():
	if 'user' in session:
		session.pop('user', None)
		session.pop('data', None)
		returnValue = 'Signed Out'
	else:
		returnValue = 'No one is logged in'

	return jsonify({ 'message' : returnValue})


# INSTAGRAM FUNCTIONS

# Instagram function to get basic user information
@app.route("/instagram-get-basic", methods=['GET'])
def instagramGetBasic():
	# Checking if data is stored
	if 'data' in session:

		# Creating variable equal to instagram data
		sessionData = session['data'][1]
	else:
		sessionData = 'None'
	return jsonify({ 'message' : sessionData})



# TWITTER FUNCTIONS

# Twitter function to get basic user information
@app.route("/twitter-get-basic", methods=['GET'])
def twitterGetBasic():
	# Checking if data is stored
	if 'data' in session:

		# Creating variable equal to twitter data
		sessionData = session['data'][2]
		print(sessionData['bio'])
	else:
		sessionData = 'None'
	return jsonify({ 'message' : sessionData})

if __name__ == '__main__':
	app.run(debug=True, port=5000) 