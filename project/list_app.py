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
    if session.get('user_id'):
        query = model.db_session.query(model.User)
        user = query.filter_by(id = session['user_id']).one()

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/test_json")
def test_json():
    return render_template("countries.json")

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
    if session.get('user_id'):
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
        
        all_tags = model.db_session.query(model.Tag).all()
        db_tag_list = []
        for each_tag in all_tags:
            db_tag_list.append(each_tag.tag_text)

        return render_template("newlist.html", db_tag_list=db_tag_list)

    elif request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        url = request.form["url"]
        public = request.form["public-list"]
        uploaded_file = request.files["file"]

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

@app.route("/first_rows/")
def first_rows():

    # uploaded_file = request.files["file"]
    uploaded_file = open("test_genelist.csv")

    if uploaded_file:
        sep = ','
    # if uploaded_file and allowed_file(uploaded_file.filename):
        
    #     filename = uploaded_file.filename
    #     file_ext = filename.rsplit('.', 1)[1]
    #     if file_ext == 'csv':
    #         sep = ','
    #     elif file_ext == ('tsv' or 'txt'):
    #         sep = '\t'

        # read in first 5 rows of uploaded file for preview
        preview_dict = {}

        header = uploaded_file.readline()
        header_list = header.rstrip().split(sep)
        preview_dict[0] = header_list

        for i in range(1,6):
            row = uploaded_file.readline().rstrip().split(sep)
            if row:
                preview_dict[i] = row
            else:
                break

    return render_template("_first_rows.html", preview_dict = preview_dict)

@app.route("/check_list/<int:column_index>")
def check_list(column_index):

    # create dictionary of valid entrez_gene_id for latest version in db
    db_entrez_gene_id_dict = {}
    max_version_id = model.get_attr_max(model.db_session, model.Version.id, 0)
    all_genes = model.db_session.query(model.geneVersion).filter_by(version_id=max_version_id).all()
    for each_gene in all_genes:
        db_entrez_gene_id_dict[each_gene.gene.entrez_gene_id] = 1

    uploaded_file = open("test_genelist.csv")

    header = uploaded_file.readline()

    egeneid_dict = {}
    egeneid_dict['pass'] = {}
    egeneid_dict['not_valid'] = []   # to store (row num, value) that are not valid gene id
    egeneid_dict['non_int'] = []     # to store (row num, value) that are not integers
    egeneid_dict['dups'] = []

    row_num = 0
    for row in uploaded_file:
        row_num += 1
        egeneid = row.rstrip().split(',')[column_index]   
        if egeneid:
            try:
                convert_to_int = int(egeneid)
                if convert_to_int in db_entrez_gene_id_dict:
                    egeneid_dict['pass'][convert_to_int] = egeneid_dict['pass'].get(convert_to_int, 0) + 1
                    print (row_num, egeneid, 'tryif')
                else:
                    egeneid_dict['not_valid'].append( (row_num, egeneid) )
                    print (row_num, egeneid, 'tryelse')
            except ValueError:
                egeneid_dict['non_int'].append( (row_num, egeneid) )
                print (row_num, egeneid, 'except')

    for key, value in egeneid_dict['pass'].iteritems():
        if value > 1:
            egeneid_dict['dups'].append(key)

    return render_template("_check_list.html", egeneid_dict = egeneid_dict)

@app.route("/check_list_sql/<int:column_index>")
def check_list_sql(column_index):

    stamp = session['username'] + str(datetime.datetime.utcnow().strftime("%s"))

    uploaded_file = open("test_genelist.csv")

    header = uploaded_file.readline()

    row_num = 0
    for row in uploaded_file:
        row_num += 1
        egeneid = row.rstrip().split(',')[column_index]
        tempgene = model.tempGene(row_num = row_num,
                            temp_gene_id = egeneid,
                            stamp = stamp )
        model.db_session.add(tempgene)
    model.db_session.commit()

    connect_to_db() 

    dup_sql = """   SELECT temp_gene_id
                    FROM tempgenes
                    WHERE stamp = ?
                    GROUP BY temp_gene_id
                    HAVING count(*) > 1 """ 

    CURSOR.execute(dup_sql, (stamp,))
    dups = CURSOR.fetchall()

    val_sql = """   SELECT row_num, temp_gene_id
                    FROM tempgenes tg
                    LEFT OUTER JOIN (
                        SELECT entrez_gene_id 
                        FROM genes g
                        INNER JOIN gene_version gv 
                            ON (g.id = gv.gene_id)
                        INNER JOIN versions v 
                            ON (v.id = gv.version_id)
                        WHERE v.id IN (
                        SELECT max(id) 
                        FROM versions)
                        ) g
                        ON (tg.temp_gene_id = g.entrez_gene_id)
                    WHERE g.entrez_gene_id IS NULL
                    AND stamp = ? """
    CURSOR.execute(val_sql, (stamp,))
    invalid = CURSOR.fetchall()

    CURSOR.close()

    egeneid_dict = {}
    egeneid_dict['not_valid'] = []   # to store (row num, value) that are not valid gene id
    egeneid_dict['dups'] = []

    for item in dups:
        egeneid_dict['dups'].append(item[0])

    for item in invalid:
        egeneid_dict['not_valid'].append((item[0], item[1]))

    return render_template("_check_list.html", egeneid_dict = egeneid_dict)

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

@app.route("/search/", methods = ["GET"])
def search():

    allowed_terms = get_accessible_search_terms_by_user_id(session['user_id'])

    search_index = []
    for term in allowed_terms:
        term_dict = {}
        term_dict['category'] = term[0]
        term_dict['value'] = term[1]
        search_index.append(term_dict)

    return render_template("search.html", search_index=search_index)

@app.route("/search_index/", methods = ["GET"])
def search_index():

    allowed_terms = get_accessible_search_terms_by_user_id(session['user_id'])

    search_index = []
    for term in allowed_terms:
        term_dict = {}
        term_dict['category'] = term[0]
        term_dict['value'] = term[1]
        search_index.append(term_dict)

    return render_template("search_index.json", search_index=search_index)

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

def get_accessible_search_terms_by_user_id(user_id):
    # limit search index displayed to subset that are in lists that user is authorized to access
    connect_to_db()
    sql = """   SELECT DISTINCT vsi.category, vsi.value FROM V_SEARCH_INDEX vsi 
                INNER JOIN (
                    SELECT DISTINCT list_id 
                    FROM v_user_lists_access 
                    WHERE owner_uid = ? or shared_uid = ? or public = 1
                    ) l
                    ON vsi.list_id = l.list_id
                ORDER BY vsi.category, vsi.value    """ 
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
    