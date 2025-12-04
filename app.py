# from flask import Flask
# from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import check_password_hash, generate_password_hash

# from helpers import apology, login_required, lookup, usd
# app = Flask(__name__)
# db = SQLAlchemy("sqlite:///finance.db")

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     # Forget any user_id
#     session.clear()

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":
#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)

#         # Query database for username
#         rows = db.execute(
#             "SELECT * FROM users WHERE username = ?", request.form.get("username")
#         )

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(
#             rows[0]["hash"], request.form.get("password")
#         ):
#             return apology("invalid username and/or password", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")


# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")


from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    
    # Get user's groups
    user = User.query.get(session["user_id"])
    memberships = GroupMember.query.filter_by(user_id=user.id).all()
    groups = [m.group for m in memberships]
    
    return render_template("index.html", groups=groups)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # Validation
        if not username or not password:
            return "Username and password required", 400
        
        if password != confirmation:
            return "Passwords must match", 400
        
        # Check if username exists
        if User.query.filter_by(username=username).first():
            return "Username already exists", 400
        
        # Create new user
        hash = generate_password_hash(password)
        new_user = User(username=username, hash=hash)
        db.session.add(new_user)
        db.session.commit()
        
        session["user_id"] = new_user.id
        session["username"] = new_user.username
        return redirect("/")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.hash, password):
            return "Invalid credentials", 403
        
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)