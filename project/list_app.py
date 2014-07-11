from flask import Flask, render_template, redirect, request, session, flash
import jinja2
import model
import datetime

UPLOAD_FOLDER = "/userUploads"
ALLOWED_EXTENSIONS = set(['txt','csv'])

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        file = request.files['InputFile']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER']), filename)
            first_rows = file.readline(5)
            print first_rows

        # append to table: list
        # append to table: list_user
        # append to table: list_tag

        return redirect("/view")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/view", methods = ["GET", "POST"])
def view():

    # get lists that are owned by current user
    if session['user_id']:
        query = model.db_session.query(model.User)
        user = query.filter_by(id = session['user_id']).one()
        genelists = user.lists      # array of List objects for the user

    # get lists that are shared with current user
    shared_query = model.db_session.query(model.listAccess)
    shared_ls_acc = shared_query.filter_by(user_id = session['user_id']).all()
    print shared_ls_acc
    if shared_ls_acc:
        for ls_acc in shared_ls_acc:
            genelists.append(ls_acc.lists)
            print len(genelists)    

    # get lists that are public and not owned by current user
    public_query = model.db_session.query(model.List)
    public_lists = public_query.filter_by(public=1).all()
    print public_lists
    for public_list in public_lists:
        if public_list.user_id != session['user_id']:
            genelists.append(public_list)
            print genelists

        list_dict = {}          # dict with List objects and array of tags
        key = 1
        for genelist in genelists:
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
            item_dict['user_id'] = user_id

            list_dict[key] = item_dict
            key += 1

        return render_template("view.html", list_dict = list_dict)

    else:
        flash('You must be logged in to view and search')
        return redirect("/login")

@app.route("/list_details")
def list_details():
    list_id = 2
    genelist = model.db_session.query(model.List).filter_by(id=list_id).one()
    return render_template("_list_details.html", list = genelist)

@app.route("/ideogram", methods = ["GET"])
def show_signup():
    return render_template("Ideogram.html")

if __name__ == "__main__":
    app.run(debug = True, port = 5000)