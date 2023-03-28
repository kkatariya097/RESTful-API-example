from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Assignment 1 : Kavya Janak Katariya (6159138) To: Professor Denis Rinfret'


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


# Student data
@app.route('/api/students')
def get_students():
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from student;")
    students = [dict(row) for row in cur]
    con.close()
    return students


# Student data by id
@app.route('/api/students/<int:student_id>')
def get_student(student_id):
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"select * from student where sid = {student_id};")
    student = dict(cur.fetchone())
    con.close()
    return student


# Student data POST
@app.route('/api/students', methods=['POST'])
def post_student():
    data = request.json
    s_id = data.get('sid', None)
    name = data.get('name', None)
    email = data.get('email', None)
    program = data.get('program', None)

    if not name:
        return {'success': False,
                'sid': int(s_id) if s_id else None,
                'msg': 'Missing name'}, 409

    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if s_id:
        statement = f"insert into student(sid, name, email, program) values ({s_id}, '{name}', '{email}', '{program}');"
    else:
        statement = f"insert into student(name, email, program) values ('{name}', '{email}' '{program}') returning s_id;"
    try:
        cur.execute(statement)
    except sqlite3.IntegrityError as e:
        con.close()
        return {'success': False,
                's_id': int(s_id),
                'msg': 'A student with this id already exists'}, 409
    if not s_id:
        s_id = cur.fetchone()[0]
    con.commit()
    con.close()
    return {'success': True, 's_id': int(s_id)}, 200


# Student data DELETE by sid
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"SELECT * FROM student WHERE sid = {student_id};")
    student = cur.fetchone()
    if not student:
        con.close()
        return {'success': False,
                'student_id': student_id,
                'msg': 'A student with this id does not exist'}, 409
    statement = f"DELETE FROM student WHERE sid = {student_id};"
    try:
        cur.execute(statement)
        con.commit()
        con.close()
        return {'success': True, 'student_id': student_id}, 200
    except sqlite3.IntegrityError as e:
        con.close()
        return {'success': False,
                'student_id': student_id,
                'msg': str(e)}, 409


# -------------------------------------------------------------------------------------------------------

# Course data
@app.route('/api/courses')
def get_courses():
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from course;")
    course = [dict(row) for row in cur]
    con.close()
    return course


# Course data by id
@app.route('/api/courses/<int:course_id>')
def get_course(course_id):
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"select * from course where cid = {course_id};")
    course = dict(cur.fetchone())
    con.close()
    return course


# Course data POST
@app.route('/api/courses', methods=['POST'])
def post_course():
    data = request.json
    c_id = data.get('cid', None)
    name = data.get('name', None)
    code = data.get('code', None)
    credit = data.get('credits', None)

    if not name:
        return {'success': False,
                'cid': int(c_id) if c_id else None,
                'msg': 'Missing Course name'}, 409

    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if c_id:
        statement = f"insert into course(cid, name, code, credits) values ({c_id}, '{name}', '{code}', '{credit}');"
    else:
        statement = f"insert into course(name, code, credits) values ('{name}', '{code}' '{credit}') returning c_id;"
    try:
        cur.execute(statement)
    except sqlite3.IntegrityError as e:
        con.close()
        return {'success': False,
                'c_id': int(c_id),
                'msg': 'A course with this id already exists'}, 409
    if not c_id:
        c_id = cur.fetchone()[0]
    con.commit()
    con.close()
    return {'success': True, 'c_id': int(c_id)}, 200


# Course data DELETE by cid
@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"SELECT * FROM course WHERE cid = {course_id};")
    course = cur.fetchone()
    if not course:
        con.close()
        return {'success': False,
                'course_id': course_id,
                'msg': 'A course with this id does not exist'}, 409
    statement = f"DELETE FROM course WHERE cid = {course_id};"
    try:
        cur.execute(statement)
        con.commit()
        con.close()
        return {'success': True, 'course_id': course_id}, 200
    except sqlite3.IntegrityError as e:
        con.close()
        return {'success': False,
                'course_id': course_id,
                'msg': str(e)}, 409


# -------------------------------------------------------------------------------------------------------


# Instructor data
@app.route('/api/instructors')
def get_instructors():
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from instructor;")
    instructor = [dict(row) for row in cur]
    con.close()
    return instructor


# Instructor data by iid
@app.route('/api/instructors/<int:instructor_id>')
def get_instructor(instructor_id):
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"select * from instructor where iid = {instructor_id};")
    instructor = dict(cur.fetchone())
    con.close()
    return instructor


# Instructor data POST
@app.route('/api/instructors', methods=['POST'])
def post_instructor():
    data = request.json
    i_id = data.get('iid', None)
    name = data.get('name', None)
    email = data.get('email', None)
    department = data.get('department', None)

    if not name:
        return {'success': False,
                'iid': int(i_id) if i_id else None,
                'msg': 'Missing name'}, 409

    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if i_id:
        statement = f"insert into instructor(iid, name, email, department) values ({i_id}, '{name}', '{email}', '{department}');"
    else:
        statement = f"insert into instructor(name, email, department) values ('{name}', '{email}' '{department}') returning i_id;"
    try:
        cur.execute(statement)
    except sqlite3.IntegrityError as e:
        con.close()
        return {'success': False,
                'i_id': int(i_id),
                'msg': 'A instructor with this id already exists'}, 409
    if not i_id:
        s_id = cur.fetchone()[0]
    con.commit()
    con.close()
    return {'success': True, 'i_id': int(i_id)}, 200


# Instructor data DELETE by iid
@app.route('/api/instructors/<int:instructor_id>', methods=['DELETE'])
def delete_instructor(instructor_id):
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"SELECT * FROM instructor WHERE iid = {instructor_id};")
    instructor = cur.fetchone()
    if not instructor:
        con.close()
        return {'success': False,
                'instructor_id': instructor_id,
                'msg': 'A instructor with this id does not exist'}, 409
    statement = f"DELETE FROM instructor WHERE iid = {instructor_id};"
    try:
        cur.execute(statement)
        con.commit()
        con.close()
        return {'success': True, 'instructor_id': instructor_id}, 200
    except sqlite3.IntegrityError as e:
        con.close()
        return {'success': False,
                'student_id': instructor_id,
                'msg': str(e)}, 409


# -------------------------------------------------------------------------------------------------------


# Offering data
@app.route('/api/offerings')
def get_offerings():
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from offering;")
    offering = [dict(row) for row in cur]
    con.close()
    return offering


# Offering data by oid
@app.route('/api/offerings/<int:offering_id>')
def get_offering(offering_id):
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"select * from offering where oid = {offering_id};")
    offering = dict(cur.fetchone())
    con.close()
    return offering


# Offering data POST
@app.route('/api/offerings', methods=['POST'])
def post_offerings():
    data = request.json
    o_id = data.get('oid', None)
    semester = data.get('semester', None)
    year = data.get('year', None)
    section = data.get('section', None)
    cid = data.get('cid', None)
    iid = data.get('iid', None)

    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if o_id:
        statement = f"insert into offering(oid, semester, year, section, cid, iid) values ('{o_id}', '{semester}', '{year}', '{section}', '{cid}', '{iid}');"
    else:
        statement = f"insert into offering(oid, semester, year, section, cid, iid) values ('{o_id}', '{semester}', '{year}', '{section}', '{cid}', '{iid}');"
    try:
        cur.execute(statement)
    except sqlite3.IntegrityError as e:
        con.close()
        return {'success': False,
                'o_id': int(o_id),
                'msg': 'A offering with this id already exists'}, 409
    if not o_id:
        o_id = cur.fetchone()[0]
    con.commit()
    con.close()
    return {'success': True, 'o_id': int(o_id)}, 200


# Offering data DELETE by oid
@app.route('/api/offerings/<int:offering_id>', methods=['DELETE'])
def delete_offering(offering_id):
    con = sqlite3.connect('data/university.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"SELECT * FROM offering WHERE oid = {offering_id};")
    offering = cur.fetchone()
    if not offering:
        con.close()
        return {'success': False,
                'offering_id': offering_id,
                'msg': 'A offering with this id does not exist'}, 409
    statement = f"DELETE FROM offering WHERE oid = {offering_id};"
    try:
        cur.execute(statement)
        con.commit()
        con.close()
        return {'success': True, 'offering_id': offering_id}, 200
    except sqlite3.IntegrityError as e:
        con.close()
        return {'success': False,
                'offering_id': offering_id,
                'msg': str(e)}, 409


if __name__ == '__main__':
    app.run()
