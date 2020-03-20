from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cs340_tornattm:2266@classmysql.engr.oregonstate.edu:3306/cs340_tornattm'
engine = create_engine('mysql+pymysql://cs340_tornattm:2266@classmysql.engr.oregonstate.edu:3306/cs340_tornattm')
db = SQLAlchemy(app)

class student(db.Model):
	first_name = db.Column(db.String(255))
	last_name = db.Column(db.String(255))
	student_id = db.Column(db.Integer, primary_key=True)
	year = db.Column(db.Integer)
	major = db.Column(db.String(255))
	email = db.Column(db.String(255))
	school_name = db.Column(db.String(255))

	def __repr__(self):
		return "<Title: {}>".format(self.first_name)

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

@app.route('/students', methods=["GET","POST"])
def students():
	all_students = db.engine.execute("SELECT * FROM student;")

	if request.form:

		if request.form.get("update_toggle"):
			update_id = request.form.get("student_id_input")
			update_fname = request.form.get("student_fname_input")
			update_lname = request.form.get("student_lname_input")
			update_year = request.form.get("student_year_input")
			update_major = request.form.get("student_major_input")
			update_email = request.form.get("student_email_input")
			update_school = request.form.get("student_school_name_input")
			db.engine.execute("UPDATE student SET student_id = '%s', first_name = '%s', last_name = '%s', year = '%s',  major = '%s', email = '%s', school_name = '%s' WHERE student_id = '%s';" %(update_id, update_fname, update_lname, update_year, update_major, update_major, update_school, update_id))

		elif request.form.get("student_id_input"):
			new_student=student(student_id=request.form.get("student_id_input"), first_name=request.form.get("student_fname_input"),
			last_name=request.form.get("student_lname_input"), year=request.form.get("student_year_input"), major=request.form.get("student_major_input"), email=request.form.get("student_email_input"), school_name=request.form.get("student_school_name_input"))
			db.session.add(new_student)
			db.session.commit()
			return(redirect('/students'))
		
		elif request.form.get("delete_student"):
			delete_student = request.form.get("delete_student")
			db.engine.execute("DELETE FROM student WHERE student_id = '%s';" %(delete_student))

	return render_template('students.html',student_list=all_students)

@app.route('/schools')
def schools():
	school_data = db.engine.execute("SELECT school_name, division FROM school;")
	return render_template('schools.html', school_list=school_data)

if __name__ == "__main__":
	app.run(debug=True)
