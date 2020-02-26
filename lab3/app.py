from ariadne import QueryType, graphql_sync, make_executable_schema, MutationType, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify

type_defs = """
    type Query {
        hello: String!
        students(id:Int!): Student!
        classes(id: Int!): Class!
    }

    type Mutation {
        createStudent(name: String!): Student!
        createClass(name: String!): Class!
        addStudentToClass(studentId: Int!, classId: Int!): Class!
    }

    type Student {
        id: Int!
        name: String!
    }

    type Class {
        id: Int!
        name: String!
        students: [Student]!
    }
"""

query = QueryType()
mutation = MutationType()
student = ObjectType("Student")

students = {}
id = 0
classid = 99999
classes = {}

"""
# Request
{hello}

#Response
{
  "data": {
    "hello": "Hello, Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36!"
  }
}
"""
@query.field("hello")
def resolve_hello(_, info):
    request = info.context
    user_agent = request.headers.get("User-Agent", "Guest")
    return "Hello, %s!" % user_agent

"""
# Request
mutation {
	createStudent(name: "Foo") {
    name
    id
  }
}

#Response
{
  "data": {
    "createStudent": {
      "id": 1,
      "name": "Foo"
    }
  }
}
"""
@mutation.field("createStudent")
def resolve_createStudent(_, info, name):
    global id
    id += 1
    students[id] = name
    return {"id" : id, "name" : name}

"""
# Request
query  {
  students(id:1) {
    name
  }
}

#Response
{
  "data": {
    "students": {
      "name": "Foo"
    }
  }
}
"""
@query.field("students")
def resolve_getStudent(_, info, id):
    return {"name" : students[id]}

"""
# Request
mutation{
  createClass(name: "test1") {
    id
    name
    students{
      name
      id
    }
  }
}

#Response
{
  "data": {
    "createClass": {
      "id": 100000,
      "name": "test1",
      "students": []
    }
  }
}
"""
@mutation.field("createClass")
def resolve_createClass(_, info, name):
    global classid
    classid += 1
    classObject = {"id" : classid, "name" : name, "students" : []}
    classes[classid] = classObject
    return classObject

"""
# Request
  query  {
    classes(id:100000) {
      name
      id
      students{
        name
        id
      }
    }
  }

#Response
{
  "data": {
    "classes": {
      "id": 100000,
      "name": "test1",
      "students": []
    }
  }
}
"""
@query.field("classes")
def resolve_classes(_, info, id):
    return classes[int(id)]

"""
# Request
  mutation  {
    addStudentToClass(studentId: 1, classId: 100000) {
      id
      name
      students{
        name
        id
      }
    }
  }

#Response
{
  "data": {
    "addStudentToClass": {
      "id": 100000,
      "name": "test1",
      "students": [
        {
          "id": 1,
          "name": "Foo"
        }
      ]
    }
  }
}

"""
@mutation.field("addStudentToClass")
def resolve_addStudentToClass(_, info, studentId, classId):
    classObject = classes[int(classId)]
    if "students" in classObject:
        studentList = classObject["students"]
        studentList.append({
                "id" : studentId,
                "name" : students[int(studentId)]
        })
    else:
        classObject["students"] = [
                {
                    "id" : studentId,
                    "name" : students[int(studentId)]
                }
            ]

    classes[classId] = classObject
    print(classes[classId])
    return classes[classId]

schema = make_executable_schema(type_defs, query, mutation, student)

app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True)