from flask import Flask
app = Flask(__name__)

@app.route("/")
def welcome():
    return "Hello! Welcome to Python Flask Demo."

@app.route("/home")
def home():
    return "This is Home Page Aka Landing Page"


from controller import *
