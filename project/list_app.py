from flask import Flask, render_template, redirect, request, session, flash
import jinja2
import model
import datetime

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

@app.before_request
def setup_session():
    session['user_id'] = session.get('user_id', None)
    session['username'] = session.get('username', None)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")

    elif request.method == "POST":

        email = request.form['email']
        username = request.form['username']

        query = model.db_session.query(model.User)

        if query.filter_by(email = email).first() is not None:
            flash('Account already exists for %s.  Please login with your credentials' % email)
            return redirect("/login")
        elif query.filter_by(username = username).first() is not None:
            flash('Account already exists for %s.  Please select a different username.' % username)
            return redirect("/signup")
        else:
            max_user_id = get_max_id(model.db_session, model.User.id)
            user = model.User(id = max_user_id +1, 
                    username=request.form["username"], password = request.form["password"], 
                    firstname = request.form["firstname"], lastname = request.form["lastname"],
                    email = request.form["email"], date = datetime.datetime.utcnow() )  
            model.db_session.add(user)
            model.db_session.commit()

            session['user_id'] = user.id
            return redirect("/view")

@app.route("/login", methods = ["GET"])
def show_login():
    if session['username']:
        flash ("You are currently logged in as: %s" % session['username'])
        return redirect ("/view")
    else:
        return render_template("login.html")

@app.route("/login", methods = ["POST"])
def process_login():
    username = request.form["username"]
    password = request.form["password"]

    query = model.db_session.query(model.User)
    user = query.filter_by(username = username).one()

    if user.password != password:
        flash ("Password incorrect, unable to login.  Please try again.")
        return render_template("login.html")

    else:
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect("/view")

@app.route("/user")
def get_user_info():
    query = model.db_session.query(model.User)
    user = query.filter_by(id = session['user_id']).one()
    user_dict = {}
    for attr, value in user.__dict__.iteritems():
        user_dict[attr] = value

    return render_template("user.html", user_dict = user_dict)

@app.route("/logout", methods=["GET"])
def show_logout():
    session.clear()
    session['user_id'] = None
    session['username'] = None
    return render_template("index.html")

@app.route("/newlist", methods = ["GET", "POST"])
def enter_new():

    if request.method == "GET":
        return render_template("newlist.html")

    elif request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        # append to table: list
        # append to table: list_user
        # append to table: list_tag

        return redirect("/view")

@app.route("/view", methods = ["GET", "POST"])
def view():

    if session['user_id']:
        query = model.db_session.query(model.User)
        user = query.filter_by(id = session['user_id']).one()
        genelists = user.lists      # array of List objects for the user
        list_dict = {}          # dict with List objects and array of tags
        for i in range(len(genelists)):
            item_dict = {}
            item_dict['list_obj'] = genelists[i]
            list_tag = genelists[i].list_tag
            tag_array =[]
            for j in range(len(list_tag)):
                tag_id = list_tag[j].tag_id
                tag = model.db_session.query(model.Tag).filter_by(id = tag_id).one()
                tag_array.append(tag)
            item_dict['tag_array'] = tag_array
            list_dict[i] = item_dict

        return render_template("view.html", list_dict = list_dict, owner = user)

    else:
        flash('You must be logged in to view and search')
        return redirect("/login")

@app.route("/ideogram", methods = ["GET"])
def show_signup():
    return render_template("Ideogram.html")

if __name__ == "__main__":
    app.run(debug = True, port = 5000)