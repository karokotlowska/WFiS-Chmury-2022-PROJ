from flask import Flask, render_template, request, jsonify
from connection import Connection
# from connection import Connection
# from employee import show_employee
# from hire import add_employee

app = Flask(__name__)
# app.register_blueprint(show_employee, url_prefix='')
# app.register_blueprint(add_employee, url_prefix='')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/createProjectForm")
def createProjectForm():
    return render_template('createProjectForm.html')

@app.route("/createProject", methods=['GET', 'POST'])
def createProject():
    db = Connection()

    if request.method == 'POST':
        new_project = {
            "name":request.form.get("name"),
            "subject":request.form.get("subject")

        }
        db.add_project(new_project)
        msg = f"Zapisano projekt"
    return render_template('index.html', msg = msg)


@app.route("/showProjects", methods=['GET', 'POST'])
def showProjects():
    db = Connection()

    if request.method == 'GET':
        projects = db.list_all()
        print(projects)
        return render_template('index.html', projects = projects)



@app.route("/addStudentForm")
def addStudentForm():
    db = Connection()
    if request.method == 'GET':
        all = db.list_all()
        all = [proj["name"] for proj in all]
        print(all)
        return render_template('index.html', projects_list = all)

@app.route('/addStudent', methods=['GET', 'POST'])
def addStudent():
    db = Connection()

    if request.method == 'POST':
        new_student = {
            "first":request.form.get("first"),
            "last":request.form.get("last"),
            "department":request.form.get("department")
        }
        project = request.form.get("project").split(' ')
        project = ' '.join(map(str, project))

        if new_student.get("first") and new_student.get("last") and new_student.get("department") and project:
            project_name = project
            db.add_student(new_student)
            db.add_relation(project_name, new_student.get("first"), new_student.get("last"))
            return render_template('index.html', msg="Dodano studenta do projektu")

        else:
            return render_template('index.html', msg="Nie udało się dodać studenta")


@app.route("/searchStudentsProjectsForm")
def searchStudentsProjectsForm():
    db = Connection()
    if request.method == 'GET':
        all = db.list_all()
        all = [proj["name"] for proj in all]
        print(all)
        return render_template('index.html', search_projects = all)
        

@app.route("/showStudentsProjects", methods=['GET', 'POST'])
def showStudentsProjects():
    db = Connection()

    project = request.form.get("project").split(' ')
    project = ' '.join(map(str, project))
    if request.method == 'POST':
        students = db.list_students(project)
        print("list students", students)
        return render_template('index.html', students = students)

@app.route("/showStudentsProjectsForm")
def showStudentsProjectsForm():
    db = Connection()
    if request.method == 'GET':
        all = db.list_all_students()
        all = [proj["firstname"] + " " + proj["lastname"] for proj in all]
        return render_template('index.html', search_students = all)
        

@app.route("/showStudentProjects", methods=['GET', 'POST'])
def showStudentProjects():
    db = Connection()
    student = request.form.get("project").split(' ')
    if request.method == 'POST':
        projects = db.list_projects(student[0]) #pierwsze imie
        if (len(projects) == 0 ):
            return render_template('index.html', msg = "Ten student nie ma jeszcze żadnych projektów")
        return render_template('index.html', projects = projects)


@app.route("/updateProjectForm")
def updateProjectForm():
    db = Connection()
    if request.method == 'GET':
        all = db.list_all()
        all = [proj["name"] for proj in all]
        return render_template('index.html', search_projects2 = all)

if __name__ == '__main__':
    app.run()