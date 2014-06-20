from flask import Flask, render_template, request #import Flask class
import hackbright_app

app = Flask(__name__) # instance of Flask class

@app.route("/")
def get_github():
    return render_template("get_github.html")

# get student by github
@app.route("/student") # route() is a decorator that tells Flask what URL should trigger function
def get_student(): # function name
    hackbright_app.connect_to_db()
    student_github = request.args.get("student") #getting key:value from url
    row = hackbright_app.get_student_by_github(student_github)
    html = render_template("student_info.html", first_name = row[0], # render_template(name_template_file, values_to_fill)
                                                last_name = row[1],
                                                github = row[2])
    return html

# get all grades by student
@app.route("/grade")
def get_grade():
    hackbright_app.connect_to_db()
    student_github = request.args.get("student")
    rows = hackbright_app.get_grades_by_student(student_github)
    projects = [] # created a list of dictionaries for html loop
    for title, grade in rows:
        row_dict = {}
        row_dict['github'] = student_github
        row_dict['project_title'] = title
        row_dict['grade'] = grade
        projects.append(row_dict)
    html = render_template("grade_info.html", projects = projects) # set html variable 'projects' to projects dict
    return html

# gets all grades (for all students) by project
@app.route("/project")
def get_project():
    hackbright_app.connect_to_db()
    title = request.args.get("project")
    rows = hackbright_app.query_all_grades_by_project(title)
    grades = []
    for first_name, last_name, grade, github in rows:
        row_dict = {}
        row_dict['first_name'] = first_name
        row_dict['last_name'] = last_name
        row_dict['github'] = github
        row_dict['project_title'] = title
        row_dict['grade'] = grade
        grades.append(row_dict)
    print grades
    html = render_template("project_info.html", grades = grades)
    return html   


#     def get_grades_by_student(github):
#     query = """SELECT project_title, grade FROM Grades WHERE student_github = ?"""
#     DB.execute(query, (github,))
#     row = DB.fetchone()
#     return"""\
# Student: %s
# Project Grade: %s: %d""" % (github, row[0], row[1])
    

if __name__ == "__main__":
    app.run(debug=True) # .run() function runs the local server, in debug mode