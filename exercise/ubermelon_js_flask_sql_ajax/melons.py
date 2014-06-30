
"""
TODO:
add_to_cart() should be structured to have a dictionary inside another (id as outer key)
"""

from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html", melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html", display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    return render_template("cart.html")
        
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.
    
    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """
    if session.get('cart'): 
        session['cart'].append(id) 
    else:
        session['cart'] = [id]

# could add show_cart function for lines below in order to allow all computation to be done only when /cart is viewed

    melon_dict = {}

    # get quantity counts
    for i in session['cart']:
        if melon_dict.get(i):
            melon_dict[i][0] += 1
            print melon_dict[i]
        else:
            melon_dict[i] = []
            melon_dict[i].append(1)
            print melon_dict[i]

    # get melon info
    for k in melon_dict:
        result = model.get_melon_by_id(k)
        quantity = melon_dict[k][0]
        melon_dict[k].append(result.common_name)
        melon_dict[k].append(result.price)
        melon_dict[k].append(quantity*result.price)

    session['all_melon_dict'] = melon_dict 

    total = 0
    for item in melon_dict:
        total += melon_dict[item][3]
    session['total'] = total
    
    html = render_template("cart.html")
    return html

@app.context_processor
def utility_processor():
    def format_price(amount, currency=u'$'):
        return u'{0}{1:.2f}'.format(currency, amount)
    return dict(format_price=format_price)

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""

    row = model.get_customer_by_email(request.form.get('email'))
    if row:
        session['customer'] = row
        flash("Log in successful")

    return redirect("/melons")

@app.route("/logout", methods=["GET"])
def show_logout():
    session.clear()
    session['customer'] = None 
    session['cart'] = []
    return render_template("index.html")

@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

@app.route("/user")
def get_user_info():
    user_dict = model.get_user_info(session['customer'][0])
    print user_dict
    return render_template("user.html", user_dict=user_dict)

@app.route("/cart_items")
def hovercart():
    return render_template("_hovercart_items.html")

if __name__ == "__main__":

    app.run(debug=True, port=5000)
    session['customer'] = None 
    session['cart'] = []
