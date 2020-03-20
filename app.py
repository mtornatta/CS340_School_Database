from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cs340_tornattm:2266@classmysql.engr.oregonstate.edu:3306/cs340_tornattm'
db = SQLAlchemy(app)

class student(db.Model):
	first_name = db.Column(db.String(255))
	last_name = db.Column(db.String(255))
	student_id = db.Column(db.Integer, primary_key=True)
	year = db.Column(db.Integer)
	major = db.Column(db.String(255))
	email = db.Column(db.String(255))
	school_name = db.Column(db.String(255))

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/classes')
def classes():
	return render_template('classes.html')

@app.route('/teachers')
def teachers():
	return render_template('teachers.html')

@app.route('/students', methods=['POST','GET'])
def students():
	all_students = student.query.all()
	return render_template('students.html',student_list=all_students)

@app.route('/schools')
def schools():
	return render_template('schools.html')

if __name__ == "__main__":
	app.run(debug=True)