--  Leon Tran
--  Michael Tornatta
--  SQL file with data manipulation queries\
--    Query for add a new character functionality with colon : character being used to
--    denote the variables that will have data from the backend programming language
--  SELECT/READ queries

#Get all class information to be displayed
SELECT class.course_id, class.course_name, class_teacher.tid, class.number_of_students, class.available_seats FROM class LEFT JOIN class_teacher ON class.course_id = class_teacher.cid;

#Get teach information to be displayed
SELECT teacher.teacher_id, concat(first_name, ' ', last_name) AS Name, class_teacher.cid FROM teacher LEFT JOIN class_teacher ON teacher.teacher_id = class_teacher.tid;

#Get student information to be displayed
SELECT student.student_id, concat(first_name,' ', last_name) AS Name, class_student.cid FROM student LEFT JOIN class_student ON student.student_id = class_student.sid;

#Get school information
SELECT school_name, division FROM school;

#Get all many to many data
SELECT * FROM class_student;

SELECT * FROM class_teacher;

--  INSERT queries
#Insert into class
INSERT INTO class (course_id, number_of_students, available_seats, course_name, school_name) VALUES (':class_id_input', '0', ':available_seats_input:', ':course_name_input:', (SELECT school_name FROM school WHERE school_name = ':school_name_input:'));

#Insert into teacher
INSERT INTO teacher (first_name, last_name, teacher_id) VALUES (':first_name_input:', ':last_name_input:', ':teacher_id_input:');

#Insert into student
INSERT INTO student (first_name, last_name, student_id, year, major, email, school_name) VALUES (':first_name_input:', ':last_name_input:', ':student_id_input:', '1', 'Computer Science', 'johnsmith@email.com', (SELECT school_name FROM school WHERE school_name = ':school_name_input:'));

#Insert into school
INSERT INTO school (school_name, division) VALUES (':school_name_input:', ':division_input:');

#Insert into Many to Many
INSERT INTO class_student (sid, cid) VALUES ((SELECT student_id FROM student WHERE first_name = ':first_name_input:'), (SELECT course_id FROM class WHERE course_name = ':course_name_input:'));

INSERT INTO class_teacher (cid, tid) VALUES ((SELECT course_id FROM class WHERE course_name = ':course_name_input:'), (SELECT teacher_id FROM teacher WHERE first_name = ':first_name_input:'));

--  UPDATE queries
#(Most are self explanatory from here)
UPDATE class SET course_id = ':course_id_input:' AND available_seats = ':available_seats_input:' WHERE course_name = ':course_name_input:';

UPDATE teacher SET teacher_id = ':teacher_id_input:' WHERE first_name = ':first_name_input:';

UPDATE student SET student_id = ':student_id_input:' WHERE first_name = ':course_name_input:';

UPDATE school SET division = ':division_input:' WHERE school_name = ':school_name_input:';

UPDATE class_student SET sid = ':new_student_id_FK:', cid = ':new_course_id_FK:' WHERE sid = ':student_id_FK:';

UPDATE class_teacher SET cid = ':new_course_id_FK:', tid = ':new_teacher_id_FK:' WHERE sid = ':course_id_FK:';

--  DELETE queries
DELETE FROM class WHERE course_id = ':course_id_input:';

DELETE FROM teacher WHERE teacher_id = ':teacher_id_input:';

DELETE FROM student WHERE student_id = ':student_id_input:';

DELETE FROM school WHERE school_name = ':school_name_input:';

DELETE FROM class_student WHERE sid = ':student_id_input:';

DELETE FROM class_teacher WHERE cid = ':course_id_input';

-- Search Queries
