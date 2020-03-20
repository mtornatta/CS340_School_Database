from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cs340_tornattm:2266@classmysql.engr.oregonstate.edu:3306/cs340_tornattm'
engine = create_engine('mysql+pymysql://cs340_tornattm:2266@classmysql.engr.oregonstate.edu:3306/cs340_tornattm')
db = SQLAlchemy(app)

# class school(db.Model):
# 	first_name = db.Column(db.String(255))
# 	last_name = db.Column(db.String(255))
# 	student_id = db.Column(db.Integer, primary_key=True)
# 	year = db.Column(db.Integer)
# 	major = db.Column(db.String(255))
# 	email = db.Column(db.String(255))
# 	school_name = db.Column(db.String(255))

# class teacher(db.Model):
# 	first_name = db.Column(db.String(255))
# 	last_name = db.Column(db.String(255))
# 	student_id = db.Column(db.Integer, primary_key=True)
# 	year = db.Column(db.Integer)
# 	major = db.Column(db.String(255))
# 	email = db.Column(db.String(255))
# 	school_name = db.Column(db.String(255))

class school(db.Model):
	school_name = db.Column(db.String(255), primary_key=True)
	division = db.Column(db.String(255))

	def __repr__(self):
		return "<school_name: {}>".format(self.school_name)

class student(db.Model):
	first_name = db.Column(db.String(255))
	last_name = db.Column(db.String(255))
	student_id = db.Column(db.Integer, primary_key=True)
	year = db.Column(db.Integer)
	major = db.Column(db.String(255))
	email = db.Column(db.String(255))
	school_name = db.Column(db.String(255))

	def __repr__(self):
		return "<first_name: {}>".format(self.first_name)

class teacher(db.Model):
	first_name = db.Column(db.String(255))
	last_name = db.Column(db.String(255))
	teacher_id = db.Column(db.Integer, primary_key=True)

	def __repr__(self):
		return"<first_name: {}>".format(self.first_name)

class course(db.Model):
	course_id = db.Column(db.Integer, primary_key=True)
	number_of_students = db.Column(db.Integer)
	available_seats = db.Column(db.Integer)
	course_name = db.Column(db.String(255))
	school_name = db.Column(db.String(255))

	def __repr__(self):
		return"<course_name: {}>".format(self.course_name)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/classes', methods=["GET", "POST"])
def classes():
	class_data = db.engine.execute("SELECT class.course_id, class.course_name, class.number_of_students, class.available_seats, class.school_name FROM class;")

	if request.form:
		db.engine.execute("INSERT INTO class (class.course_id, class.course_name, class.number_of_students, class.available_seats, class.school_name) VALUES (%s, %s, %s, %s, (SELECT school_name FROM school WHERE school_name = %s)), %(course_id_input, course_name_input, student_input, seats_input, school_name_input);")

		#new_class=course(course_id=request.form.get("course_id_input"), course_name=request.form.get("course_name_input"), number_of_students=request.form.get("student_input"), available_seats=request.form.get("seats_input"),
		#school_name=request.form.get("school_name_input"))
		#db.session.add(new_class)
		#db.session.commit()
		return(redirect('/classes'))

	return render_template('classes.html', class_list=class_data)

@app.route('/teachers', methods=["GET","POST"])
def teachers():
	teacher_data = db.engine.execute("SELECT teacher.teacher_id, concat(first_name, ' ', last_name) AS Name, class_teacher.cid FROM teacher LEFT JOIN class_teacher ON teacher.teacher_id = class_teacher.tid;")

	if request.form:
		new_teacher=teacher(first_name=request.form.get("teacher_fname_input"), last_name=request.form.get("teacher_lname_input"), teacher_id=request.form.get("teacher_id_input"))
		db.session.add(new_teacher)
		db.session.commit()
		return(redirect('/teachers'))

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

@app.route('/schools', methods=["GET","POST"])
def schools():
	school_data = db.engine.execute("SELECT school_name, division FROM school;")

	if request.form:
		new_school=school(school_name=request.form.get("school_name_input"), division=request.form.get("school_division_input"))
		db.session.add(new_school)
		db.session.commit()
		return(redirect('/schools'))

	return render_template('schools.html', school_list=school_data)

if __name__ == "__main__":
	app.run(debug=True)
