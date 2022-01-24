from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = db.engine


class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    image = db.Column(db.String(100), unique=True)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")

    products = Products.query.all()
    return render_template("index.html", products=products)


@app.route("/cart", methods=["GET", "POST"])
def cart():
    # Ensure cart exists
    if "cart" not in session:
        session["cart"] = []
    if not session.get("name"):
        return redirect("/login")

    # POST
    if request.method == "POST":
        id = request.form.get("id")
        if id:
            session["cart"].append(id)
        return redirect("/cart")
    # GET
    products = Products.query.filter(Products.id.in_(session['cart']))
    return render_template('cart.html', products=products)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()

        # check if the user exists and the password's hash matches
        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again")
            return redirect('/login')

        session["name"] = user.name
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session['name'] = None
    session['cart'] = []
    return redirect("/")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect('/login')

        # create a new user with the form data. Hash the password
        new_user = Users(name=name, email=email, password=generate_password_hash(password, method='sha256'))

        # add the new user to the DB
        db.session.add(new_user)
        db.session.commit()

        session["name"] = name
        return redirect('/')

    return render_template("signup.html")


if __name__ == '__main__':
    app.run(debug=True)
