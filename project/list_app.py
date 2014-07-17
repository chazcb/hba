from flask import Flask, render_template, redirect, request, session, flash, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy.orm.exc import NoResultFound
import os
import jinja2
import model
import datetime
import sqlite3
import json

CONN = None
CURSOR = None

# add line below to save file to file system
# UPLOAD_FOLDER = "/home/vivien/src/hba/project/userUploads/"

ALLOWED_EXTENSIONS = set(['txt','tsv','csv'])

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

# add line below to save file to file system
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def connect_to_db():
    global CONN, CURSOR
    CONN = sqlite3.connect("repo.db")
    CURSOR = CONN.cursor() # mechanism to interact with the database, to execute queries (similar to a file handle)

@app.before_request
def setup_session():

    if session.get('user_id', None):
        query = model.db_session.query(model.User)
        user = query.filter_by(id = session['user_id']).one()

@app.route("/test")
def test():
    return render_template("test.html")

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
            max_user_id = model.get_attr_max(model.db_session, model.User.id, 0)
            user = model.User(id = max_user_id +1, 
                    username=request.form["username"], password = request.form["password"], 
                    firstname = request.form["firstname"], lastname = request.form["lastname"],
                    email = request.form["email"], date_created = datetime.datetime.utcnow() )  
            model.db_session.add(user)
            model.db_session.commit()

            session['user_id'] = user.id
            session['username'] = user.username
            return redirect("/view")

@app.route("/login", methods = ["GET"])
def show_login():
    if session['user_id']:
        flash ("You are currently logged in as: %s" % session['username'])
        return redirect ("/view")
    else:
        return render_template("login.html")

@app.route("/login", methods = ["POST"])
def process_login():
    username = request.form["username"]
    password = request.form["password"]

    query = model.db_session.query(model.User)

    try:    # if username exists
        user = query.filter_by(username = username).one()

        if user.password != password:
            flash ("Password incorrect, unable to login.  Please try again.")
            return render_template("login.html")
        else:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect("/view")

    except NoResultFound:   # if username does not exist
        flash ("%s is not a registered username.  Please try again." % username)
        return render_template("login.html")

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
        url = request.form["url"]
        public = request.form["public-list"]
        uploaded_file = request.files['file']

        if uploaded_file and allowed_file(uploaded_file.filename):

            # add 2 lines below to save file to file system
            # fn = secure_filename(uploaded_file.filename)
            # uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
            
            filename = uploaded_file.filename
            file_ext = filename.rsplit('.', 1)[1]
            if file_ext == 'csv':
                sep = ','
            elif file_ext == ('tsv' or 'txt'):
                sep = '\t'

            # read in first 5 rows of uploaded file for preview
            preview_dict = {}

            header = uploaded_file.readline()
            header_list = header.rstrip().split(sep)
            preview_dict[1] = header_list

            for i in range(1,5):
                row = uploaded_file.readline().rstrip().split(sep)
                preview_dict[i] = row

        # append to table: list
        # append to table: list_user
        # append to table: list_tag

        # return redirect("/view")
        return redirect("/")

@app.route("/tag_search")
def tag_search():
    connect_to_db() 
    sql = "SELECT tag_text FROM tags" 
    CURSOR.execute(sql, )
    rows = CURSOR.fetchall()
    CURSOR.close()

    tag_list = []
    for row in rows:
        tag_list.append(row[0])

    return render_template("_tag_search.html", tag_list=tag_list)

@app.route("/view", methods = ["GET", "POST"])
def view():

    curr_user_id = session['user_id']

    if curr_user_id:

        rows = get_accessible_lists_by_user_id(curr_user_id)
        genelists = []  # store array of List objects for current user
        for item in rows:
            query = model.db_session.query(model.List)
            accessible = query.get(item[0])
            genelists.append(accessible)

        list_dict = gen_list_dict_by_genelist(genelists, curr_user_id)

        return render_template("view.html", list_dict = list_dict)

    else:
        flash('You must be logged in to view and search')
        return redirect("/login")

@app.route("/list_details/<int:list_id>") #list_id is passed from ajax call
def list_details(list_id):
    genelist = model.db_session.query(model.List).filter_by(id=list_id).one()
    return render_template("_list_details.html", list = genelist)

@app.route("/ideogram", methods = ["GET"])
def show_signup():
    # original source:
    # return render_template("http://bioinformatics.mdanderson.org/ideogramviewer/Ideogram.html")
    # local cache
    return render_template("Ideogram.html")

def get_accessible_lists_by_user_id(user_id):
    # use SQL to retrieve (i) lists owned by current user (ii) lists that are shared with current user
    # and (iii) lists that are public and not owned by current user
    # note: need to close SQL CURSOR connection to avoid concurrent db sessions
    connect_to_db()     
    sql = """   SELECT DISTINCT list_id 
                FROM v_user_lists_access 
                WHERE owner_uid = ? or shared_uid = ? or public = 1""" 
    CURSOR.execute(sql, (user_id, user_id))
    rows = CURSOR.fetchall()
    CURSOR.close()
    return rows

def gen_list_dict_by_genelist(listobj_array, curr_user_id):

    list_dict = {}          # dict with List objects and array of tags
    key = 1
    for genelist in listobj_array:
        item_dict = {}
        # add listGene object to dict 
        item_dict['list_obj'] = genelist
        # add list of Tag objects to dict 
        list_tag = genelist.list_tag
        tag_array = []
        for ls_tag in list_tag:
            tag = ls_tag.tag
            tag_array.append(tag)
        item_dict['tag_array'] = tag_array
        # add string of concatentated gene symbols to dict
        list_gene = genelist.list_gene
        genesym_array = []
        for ls_gene in list_gene:
            gene = ls_gene.gene
            genesym_array.append(gene.entrez_gene_symbol)
        item_dict['genesym'] = ','.join(genesym_array)
        # add username to dict
        user_id = genelist.user_id
        item_dict['user'] = model.db_session.query(model.User).get(user_id)
        # add group (own, shared, public) to dict
        shared = model.db_session.query(model.listAccess).filter_by(list_id=genelist.id).all()
        if genelist.user_id == curr_user_id:
            item_dict['group'] = "Your lists"
        elif shared:
            for shared_list in shared:
                if shared_list.user_id == curr_user_id:               
                    item_dict['group'] = "Shared lists"
        elif genelist.public == 1:
            item_dict['group'] = "Public lists"

        list_dict[key] = item_dict
        key += 1

    return list_dict

def allowed_file(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS)

if __name__ == "__main__":
    app.run(debug = True, port = 5000)
    