from flask import Flask, render_template, redirect, request, session, flash
import model
import jinja2
import datetime

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

@app.before_request
def setup_session():
    session['user_id'] = session.get('user_id', None)

@app.route("/")
def index():
    user_list = model.db_session.query(model.User).limit(5).all()

    return render_template("index.html", users=user_list)

@app.route("/ideogram", methods = ["GET"])
def show_signup():

    return render_template("Ideogram.html")

@app.route("/signup", methods=["POST"])
def signup():

    user = model.User(username=request.form["username"], password = request.form["password"], 
            firstname = request.form["firstname"], lastname = request.form["lastname"],
            email = request.form["email"], date = datetime.datetime.today())  
    model.db_session.add(user)
    model.db_session.commit()

    return redirect("/")

@app.route("/login", methods = ["GET"])
def show_login():
    return render_template("login.html")

@app.route("/login", methods = ["POST"])
def process_login():
    username = request.form["username"]
    password = request.form["password"]

    query = model.db_session.query(model.User)
    user = query.filter_by(username = username).one()

    if user.password != password:

        print "Password incorrect, unable to login"
        return render_template("login.html")

    else:

        session['user_id'] = user.id
 
        return redirect("/")


if __name__ == "__main__":
    app.run(debug = True, port = 5000)