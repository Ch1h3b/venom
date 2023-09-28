import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from routes import *

with app.app_context():
    db.create_all()

    
if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")


