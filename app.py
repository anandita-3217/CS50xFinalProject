from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# Import db and models from models.py
from models import db, User, Group, GroupMember, Expense, Debt

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db with app
db.init_app(app)

# Routes
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    
    # Get user's groups
    memberships = GroupMember.query.filter_by(user_id=session["user_id"]).all()
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


@app.route("/create-group", methods=["GET", "POST"])
def create_group():
    if "user_id" not in session:
        return redirect("/login")
    
    if request.method == "POST":
        name = request.form.get("name")
        theme = request.form.get("theme", "default")
        
        if not name:
            return "Group name required", 400
        
        # Create group
        new_group = Group(name=name, theme=theme)
        db.session.add(new_group)
        db.session.commit()
        
        # Add creator as member
        membership = GroupMember(group_id=new_group.id, user_id=session["user_id"])
        db.session.add(membership)
        db.session.commit()
        
        return redirect(f"/group/{new_group.id}")
    
    return render_template("create_group.html")


@app.route("/group/<int:group_id>")
def view_group(group_id):
    if "user_id" not in session:
        return redirect("/login")
    
    group = Group.query.get_or_404(group_id)
    
    # Check if user is member
    is_member = GroupMember.query.filter_by(
        group_id=group_id, 
        user_id=session["user_id"]
    ).first()
    
    if not is_member:
        return "You are not a member of this group", 403
    
    # Get expenses
    expenses = Expense.query.filter_by(group_id=group_id).order_by(Expense.created_at.desc()).all()
    
    # Get members
    members = GroupMember.query.filter_by(group_id=group_id).all()
    
    return render_template("group.html", group=group, expenses=expenses, members=members)


if __name__ == "__main__":
    app.run(debug=True)