from flask import Flask, render_template, request, jsonify, abort
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from bson import ObjectId
from mongoengine import StringField, DateTimeField, ListField, ReferenceField, IntField, PULL
from flask_debugtoolbar import DebugToolbarExtension
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super_secret'
app.config['MONGODB_SETTINGS'] = {
    'db':   'school',
    'host': '127.0.0.1',
    'port': 27017,
    # 'username': 'test',
    # 'password': '123456'
}
bootstrap = Bootstrap(app)
db = MongoEngine(app)

app.debug = True
toolbar = DebugToolbarExtension(app)


class Grade(db.Document):
    # meta = {} # {"db_alias": "user-db", 'collection': 'grade_2'}
    name = StringField(max_length=16, required=True)
    updated_at = DateTimeField(default=datetime.datetime.now)
    students = ListField(ReferenceField('Student'))

    def __str__(self):
        return "name:%s,updated_at:%s" % (self.name, self.updated_at)


class Student(db.Document):
    # 字段
    name = StringField(max_length=32, required=True)
    gender = StringField(max_length=32, required=True)
    age = IntField(required=True)
    # grade_id = ObjectIdField()
    grade = ReferenceField('Grade')

    # 结构
    def __str__(self):
        return "name:%s,gender:%s,age:%d" % (self.name, self.gender, self.age)


@app.route('/')
def index():
    all_students = Student.objects().all()
    all_grades = Grade.objects().all()
    return render_template('index.html', students=all_students, grades=all_grades)


@app.route('/student', defaults={'student_id': None})
@app.route('/student/<student_id>')
def view_student(student_id):
    all_grades = Grade.objects().all()
    if student_id:
        student = Student.objects(id=student_id).first()
        return render_template('edit.html', student=student, grades=all_grades)
    else:
        return render_template('edit.html', grades=all_grades)


@app.route('/api/students', methods=['GET'])
def get_students():
    all_students = Student.objects().all()
    return jsonify({'students': all_students})


@app.route('/api/student/<student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.objects(id=student_id).first()
    if not student:
        return jsonify({'msg': 'no student'})
    return jsonify({'student': student})


@app.route('/api/student', methods=['POST'])
def add_student():
    # print(request.json)
    if not request.json:
        abort(400)
    json = request.json
    if 'name' not in json or 'age' not in json or 'gender' not in json or 'grade' not in json:
        abort(400)
    name = request.json['name']
    age = request.json['age']
    gender = request.json['gender']
    student = Student(name=name, age=age, gender=gender)
    student.grade = ObjectId(json['grade'])
    student.save()
    one_grade = Grade(id=json['grade'])
    one_grade.update(push__students=[student]) # push item in list
    return jsonify({'student': student}), 200


@app.route('/api/student/<student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.objects(id=student_id).first()
    if not student:
        abort(404)
    if not request.json:
        abort(400)
    json = request.json
    if 'name' not in json or 'age' not in json or 'gender' not in json or 'grade' not in json:
        abort(400)
    grade_id = ObjectId(json['grade'])
    if student.grade.id == grade_id:
        result = student.update(name=json['name'], age=json['age'], gender=json['gender'])
    else:
        result = student.update(name=json['name'], age=json['age'], gender=json['gender'], grade=grade_id)
        Grade.objects(id=student.grade.id).update_one(pull__students=student)  # Remove
        Grade.objects(id=grade_id).update_one(push__students=student)  # Add
    return jsonify({'student': result})


@app.route('/api/student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.objects(id=student_id).first()
    if not student:
        abort(404)
    Grade.objects(id=student.grade.id).update_one(pull__students=student) # Remove
    student.delete()
    return jsonify({'result': True})


@app.route('/api/grades', methods=['GET'])
def get_grades():
    all_grade = Grade.objects().all()
    # return jsonify({'grades': all_grade})
    return all_grade.to_json()


@app.route('/api/grade/<grade_id>', methods=['GET'])
def get_grade(grade_id):
    one_grade = Grade.objects(id=grade_id).first()
    return jsonify(one_grade)


if __name__ == '__main__':
    app.run(debug=True)
