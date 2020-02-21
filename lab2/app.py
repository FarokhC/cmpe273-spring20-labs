from flask import Flask, escape, request

app = Flask(__name__)

students = {}
id = 0
classid = 99999
classes = {}

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

"""
POST /students

# Request
{
    "name": "Bob Smith"
}

# Response
# HTTP Code: 201
{
    "id" : 1234456,
    "name" : "Bob Smith"
}
"""
@app.route('/students', methods = ["POST"])
def createStudent():
    global id
    id += 1
    studentName = request.args.get("name")
    print(studentName)
    students[id] = studentName
    return {"id" : id, "name" : studentName}, 201
"""
GET /students/{id}

{
    "id" : 1234456,
    "name" : "Bob Smith"
}
"""
@app.route('/students/<id>', methods = ["GET"])
def getStudent(id):
    return {
        "id:" : id,
        "name" : students[int(id)]
    }

"""
POST /classes

# Request
{
    "name": "CMPE-273"
}

# Response
{
    "id": 1122334,
    "name": "CMPE-273",
    "students": []
}
"""
@app.route('/classes', methods = ["POST"])
def createClass():
    global classid
    classid += 1
    className = request.args.get("class")
    studentIds = []
    classObject = {"id" : classid, "name" : className}
    classes[classid] = classObject
    return {
        "class": classes[classid],

    }

"""
GET /classes/{id}

{
    "id": 1122334,
    "name": "CMPE-273",
    "students": []
}
"""
@app.route("/classes/<id>", methods = ["GET"])
def retrieveClass(id):
    return classes[int(id)]

"""
PATCH /classes/{id}

# Request
{
    "student_id": 1234456
}

# Response
{
    "id": 1122334,
    "name": "CMPE-273",
    "students": [
        {   "student" {
                "id" : 1234456,
                "name" : "Bob Smith"
            }
        }
    ]
}
"""
@app.route("/classes/<id>", methods = ["PATCH"])
def addStudentToClass(id):
    student_id = request.args.get("student_id")
    class_id = id
    classObject = classes[int(class_id)]
    if "students" in classObject:
        studentList = classObject["students"]
        studentList.append({
                "id" : student_id,
                "name" : students[int(student_id)]
        })
    else:
        classObject["students"] = [
                {
                    "id" : student_id,
                    "name" : students[int(student_id)]
                }
            ]

    classes[class_id] = classObject
    return classes[class_id]
