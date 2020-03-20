from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cs340_tornattm:2266@classmysql.engr.oregonstate.edu:3306/cs340_tornattm'
engine = create_engine('mysql+pymysql://cs340_tornattm:2266@classmysql.engr.oregonstate.edu:3306/cs340_tornattm')
db = SQLAlchemy(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/classes')
def classes():
	class_data = db.engine.execute("SELECT class.course_id, class.course_name, class_teacher.tid, class.number_of_students, class.available_seats FROM class LEFT JOIN class_teacher ON class.course_id = class_teacher.cid;")
	return render_template('classes.html', class_list=class_data)

@app.route('/teachers')
def teachers():
	teacher_data = db.engine.execute("SELECT teacher.teacher_id, concat(first_name, ' ', last_name) AS Name, class_teacher.cid FROM teacher LEFT JOIN class_teacher ON teacher.teacher_id = class_teacher.tid;")
	return render_template('teachers.html',teacher_list=teacher_data)

@app.route('/students', methods=['POST','GET'])
def students():
	student_data = db.engine.execute("SELECT student.student_id, concat(first_name,' ', last_name) AS Name, class_student.cid FROM student LEFT JOIN class_student ON student.student_id = class_student.sid;")
	return render_template('students.html',student_list=student_data)

@app.route('/schools')
def schools():
	school_data = db.engine.execute("SELECT school_name, division FROM school;")
	return render_template('schools.html', school_list=school_data)

if __name__ == "__main__":
	app.run(debug=True)