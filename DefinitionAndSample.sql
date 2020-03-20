DROP TABLE IF EXISTS school;

CREATE TABLE school (
  school_name varchar(255) NOT NULL,
  division varchar(255) NOT NULL,
  PRIMARY KEY (school_name)
);

INSERT INTO school (school_name, division) VALUES ('Oregon State University', 'PAC 12');


DROP TABLE IF EXISTS student;

CREATE TABLE student (
  first_name varchar(255) NOT NULL,
  last_name varchar(255) NOT NULL,
  student_id int NOT NULL,
  year int NOT NULL,
  major varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  school_name varchar(255) NOT NULL,
  PRIMARY KEY (student_id),
  FOREIGN KEY (school_name) REFERENCES school (school_name)
);

INSERT INTO student (first_name, last_name, student_id, year, major, email, school_name) VALUES ('John', 'Smith', '123456', '1', 'Computer Science', 'johnsmith@email.com', (SELECT school_name FROM school)), ('Mary', 'Jane', '135246', '4', 'Mechanical Engineering', 'maryjane@email.com', (SELECT school_name FROM school)), ('Peter', 'Parker', '188333', '4', 'Film', 'peterparker@email.com', (SELECT school_name FROM school));

DROP TABLE IF EXISTS class;

CREATE TABLE class (
  course_id int NOT NULL,
  number_of_students int,
  available_seats int NOT NULL,
  course_name varchar(255) NOT NULL,
  school_name varchar(255) NOT NULL,
  PRIMARY KEY (course_id),
  FOREIGN KEY (school_name) REFERENCES school (school_name)
);

INSERT INTO class (course_id, number_of_students, available_seats, course_name, school_name) VALUES ('101', '3', '7', 'MTH 101', (SELECT school_name FROM school WHERE school_name = 'Oregon State University')), ('214', '2', '8', 'WR 214', (SELECT school_name FROM school WHERE school_name = 'Oregon State University'));


DROP TABLE IF EXISTS teacher;

CREATE TABLE teacher (
  first_name varchar(255) NOT NULL,
  last_name varchar(255) NOT NULL,
  teacher_id int NOT NULL,
  PRIMARY KEY (teacher_id)
);

INSERT INTO teacher (first_name, last_name, teacher_id) VALUES ('Will', 'Smith', '566777'), ('Damian', 'Lillard', '000000');

DROP TABLE IF EXISTS class_student;

CREATE TABLE class_student (
  sid int NOT NULL,
  cid int NOT NULL,
  FOREIGN KEY (sid) REFERENCES student (student_id),
  FOREIGN KEY (cid) REFERENCES class (course_id)
);

INSERT INTO class_student (sid, cid) VALUES ((SELECT student_id FROM student WHERE first_name = 'John'), (SELECT course_id FROM class WHERE course_name = 'MTH 101')), ((SELECT student_id FROM student WHERE first_name = 'John'), (SELECT course_id FROM class WHERE course_name = 'WR 214')), ((SELECT student_id FROM student WHERE first_name = 'Mary'), (SELECT course_id FROM class WHERE course_name = 'MTH 101')), ((SELECT student_id FROM student WHERE first_name = 'Mary'), (SELECT course_id FROM class WHERE course_name = 'WR 214')), ((SELECT student_id FROM student WHERE first_name = 'Peter'), (SELECT course_id FROM class WHERE course_name = 'MTH 101'));

DROP TABLE IF EXISTS class_teacher;

CREATE TABLE class_teacher (
  cid int NOT NULL,
  tid int NOT NULL,
  FOREIGN KEY (cid) REFERENCES class (course_id),
  FOREIGN KEY (tid) REFERENCES teacher (teacher_id)
);

INSERT INTO class_teacher (cid, tid) VALUES ((SELECT course_id FROM class WHERE course_name = 'MTH 101'), (SELECT teacher_id FROM teacher WHERE first_name = 'Will')), ((SELECT course_id FROM class WHERE course_name = 'WR 214'), (SELECT teacher_id FROM teacher WHERE first_name = 'Damian'));
