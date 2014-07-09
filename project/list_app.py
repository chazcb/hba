from flask import Flask, render_template, redirect, request, session, flash
import jinja2
import model
import datetime

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

@app.before_request
def setup_session():
    session['user_id'] = session.get('user_id', None)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods = ["POST"])
def signup():

    email = request.form['email']
    username = request.form['username']

    if model.db_session.query.filter(model.User.email == email).first() is not None:
        flash('Account already exists for this email address!')
        return redirect("/signup")
    elif model.db_session.query.filter(model.User.username == username).first() is not None:
        flash('Account already exists for this email address!')
        return redirect("/signup")
    else:
        max_user_id = get_max_id(model.db_session, model.User.id)
        user = model.User(id = max_user_id +1, 
                username=request.form["username"], password = request.form["password"], 
                firstname = request.form["firstname"], lastname = request.form["lastname"],
                email = request.form["email"], date = datetime.datetime.utcnow())  
        model.db_session.add(user)
        model.db_session.commit()
        return redirect("/login")

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

@app.route("/ideogram", methods = ["GET"])
def show_signup():
    return render_template("Ideogram.html")

if __name__ == "__main__":
    app.run(debug = True, port = 5000)