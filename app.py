from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import mysql.connector
from config import DB_CONFIG
import mysql.connector  
from db import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# from models.prediction import Prediction

app = Flask(__name__)

Base = declarative_base()

# This method handles connection to my database
# -def connect_to_database():
# -    try:
# -        connection = mysql.connector.connect(**DB_CONFIG)
# -        if connection.is_connected():
# -            print("Connected to the database successfully!")
# -        return connection
# -
# -    except Exception as e:
# -        print(f"Error: Could not connect to the database. Reason: {str(e)}")
# -        return None
# -
# -    finally:
# -        # Connection will be closed in the calling code after using it.
# -        pass

class Prediction(Base):
    __tablename__ = 'prediction'
    def __init__(self, league, teams, tips, result, posted_by, bet_platform, slip_code):
        self.league = league
        self.teams = teams
        self.tips = tips
        self.result = result
        self.posted_by = posted_by
        self.bet_platform = bet_platform
        self.slip_code = slip_code

def connect_to_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection

    except Exception as e:
        print(f"Error: Could not connect to the database. Reason: {str(e)}")
        return None

connection = connect_to_database()

if connection and connection.is_connected():
    connection.close()
    print("Connection closed.")


@app.route('/')
def home():
    return render_template('admin_dashboard.html') 

@app.route('/admin')
def admin():
    return render_template('admin_dashboard.html')

@app.route('/manage')
def manage():
    return render_template('admin_view_users.html')

@app.route('/add', methods=['GET', 'POST'])
def add_prediction() -> str:
    """Handles the addition of a new prediction to the database.
    
    Args:
        None
    
    Returns:
        str: The URL for the success page if the prediction is added successfully, otherwise renders the 'admin_add_slip.html' template.
    """
    if request.method == 'POST':
        league = request.form['league']
        teams = request.form['teams']
        tips = request.form['tips']
        result = request.form['result']
        posted_by = request.form['posted_by']
        bet_platform = request.form['bet_platform']
        slip_code = request.form['slip_code']

        new_prediction = Prediction(league, teams, tips, result, posted_by, bet_platform, slip_code)
        db.session.add(new_prediction)
        db.session.commit()
        print("Connection to the database is successful")

        return redirect(url_for('success'))

    return render_template('admin_add_slip.html')


@app.route('/success')
def success():
    return 'Slip added successfully!'

@app.route('/edit')
def edit():
    return render_template('admin_edit_slip.html')

@app.route('/delete')
def delete():
    return render_template('admin_delete_slip.html')


if __name__ == '__main__':
    app.run(debug=True)
