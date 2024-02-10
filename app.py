from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import mysql.connector
# from config import DB_CONFIG
import mysql.connector  
from db import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
import logging


app = Flask(__name__)
# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Adeyinka@2002',
    'database': 'three_ninjas',
}

# Construct the database URI
DB_URI = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{quote_plus(DB_CONFIG['password'])}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Initialize SQLAlchemy with the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

Base = declarative_base()


class Prediction(Base):
    __tablename__ = 'prediction'
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    league = Column(String)
    teams = Column(String)
    tips = Column(String)
    result = Column(String)
    posted_by = Column(String)
    bet_platform = Column(String)
    slip_code = Column(String)

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
def admin_dashboard():
    return render_template('admin_dashboard.html') 

# This section handles routes to take care of template rendering and the form processing 
@app.route('/add_slip', methods=['GET'])
def render_add_slip_form():
    return render_template('admin_add_slip.html')

@app.route('/submit_slip', methods=['POST'])
def submit_slip_form():
    if request.method == 'POST':
        league = request.form['league']
        teams = request.form['teams']
        tips = request.form['tips']
        result = request.form['result']
        posted_by = request.form['posted_by']
        bet_platform = request.form['bet_platform']
        slip_code = request.form['slip_code']

        new_prediction = Prediction(
            league=league,
            teams=teams,
            tips=tips,
            result=result,
            posted_by=posted_by,
            bet_platform=bet_platform,
            slip_code=slip_code
        )

        try:
            db.session.add(new_prediction)
            db.session.commit()
            logging.info('Database commit successful')
        except Exception as e:
            logging.error(f'Database commit failed: {e}')
            return "Database commit failed"

        return redirect(url_for('add_slip'))

    return render_template('admin_add_slip.html')

@app.route('/success')
def success():
    print("Database transaction successful")
    return render_template('admin_add_slip.html')

@app.route('/failed')
def failed():
    return 'Database transaction failed!'

# Everything that has to do with saving slip to the database

# Everything that has to with updating a record starts here 
@app.route('/edit_slip', methods=['GET'])
def display_edit_slip():
    return render_template('admin_edit_slip.html')

@app.route('/edit_slip/<string:game_id>', methods=['POST'])
def process_edit_slip_form(game_id):
    prediction = Prediction.query.get(game_id)
    prediction.league = request.form['league']
    prediction.teams = request.form['teams']
    prediction.tips = request.form['tips']
    prediction.result = request.form['result']
    prediction.posted_by = request.form['posted_by']
    prediction.bet_platform = request.form['bet_platform']
    prediction.slip_code = request.form['slip_code']

    db.session.commit()

    return redirect(url_for('success'))

@app.route('/delete_slip', methods=['GET'])
def display_delete_slip():
    return render_template('admin_delete_slip.html')

@app.route('/delete/<string:game_id>', methods=['POST'])
def delete_slip(game_id):
    prediction = Prediction.query.get(game_id)
    if prediction:
        db.session.delete(prediction)
        db.session.commit()
        return redirect(url_for('success'))
    else:
        # Handle if the prediction with the given ID does not exist
        return "Prediction not found", 404


@app.route('/manage_user', methods=['GET'])
def display_manage_user():
    return render_template('admin_manage_user.html')

    


if __name__ == '__main__':
    app.run(debug=True)
