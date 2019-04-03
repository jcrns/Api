# Importing all needed Flask classes
from flask import Flask, make_response 

class User:
	email = ''
	password = ''
	def __init__(self, email, password):
		self.email = email
		self.password = password

	def currentUser():
		
