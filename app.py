from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

# This method handles connection to my database
def connect_to_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Connected to the database successfully!")
        return connection

    except Exception as e:
        print(f"Error: Could not connect to the database. Reason: {str(e)}")
        return None

    finally:
        # Connection will be closed in the calling code after using it.
        pass

connection = connect_to_database()

# Perform other database operations using the 'connection' object here

if connection and connection.is_connected():
    connection.close()
    print("Connection closed.")

## Database connection ends here 


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
def add():
    if request.method == 'POST':
        league = request.form['league']
        teams = request.form['teams']
        tips = request.form['tips']
        result = request.form['result']
        posted_by = request.form['posted_by']
        bet_platform = request.form['bet_platform']
        slip_code = request.form['slip_code']

        #request payload
        new_prediction = Prediction(
            league=league,
            teams=teams,
            tips=tips,
            result=result,
            posted_by=posted_by,
            bet_platform=bet_platform,
            slip_code = slip_code
        )
        db.session.add(new_prediction)
        db.session.commit()

        return redirect(url_for('success'))

    return render_template('admin_add_slip.html')



@app.route('/success')
def success():
    return 'Slip added successfully!'
    return render_template('admin_add_slip.html')

@app.route('/edit')
def edit():
    return render_template('admin_edit_slip.html')

@app.route('/delete')
def delete():
    return render_template('admin_delete_slip.html')


if __name__ == '__main__':
    app.run(debug=True)
