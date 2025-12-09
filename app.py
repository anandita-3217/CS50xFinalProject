# from flask import Flask, render_template, request, session, redirect, url_for
# from flask_session import Session
# from werkzeug.security import check_password_hash, generate_password_hash
# from datetime import datetime

# # Import db and models from models.py
# from models import db, User, Group, GroupMember, Expense, Debt

# app = Flask(__name__)

# # Configure session
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # Configure SQLAlchemy
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# # Initialize db with app
# db.init_app(app)

# # Routes
# @app.route("/")
# def index():
#     if "user_id" not in session:
#         return redirect("/login")
    
#     # Get user's groups
#     memberships = GroupMember.query.filter_by(user_id=session["user_id"]).all()
#     groups = [m.group for m in memberships]
    
#     return render_template("index.html", groups=groups)


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         confirmation = request.form.get("confirmation")
        
#         # Validation
#         if not username or not password:
#             return "Username and password required", 400
        
#         if password != confirmation:
#             return "Passwords must match", 400
        
#         # Check if username exists
#         if User.query.filter_by(username=username).first():
#             return "Username already exists", 400
        
#         # Create new user
#         hash = generate_password_hash(password)
#         new_user = User(username=username, hash=hash)
#         db.session.add(new_user)
#         db.session.commit()
        
#         session["user_id"] = new_user.id
#         session["username"] = new_user.username
#         return redirect("/")
    
#     return render_template("register.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     session.clear()
    
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
        
#         user = User.query.filter_by(username=username).first()
        
#         if not user or not check_password_hash(user.hash, password):
#             return "Invalid credentials", 403
        
#         session["user_id"] = user.id
#         session["username"] = user.username
#         return redirect("/")
    
#     return render_template("login.html")


# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/")


# @app.route("/create-group", methods=["GET", "POST"])
# def create_group():
#     if "user_id" not in session:
#         return redirect("/login")
    
#     if request.method == "POST":
#         name = request.form.get("name")
#         theme = request.form.get("theme", "default")
        
#         if not name:
#             return "Group name required", 400
        
#         # Create group
#         new_group = Group(name=name, theme=theme)
#         db.session.add(new_group)
#         db.session.commit()
        
#         # Add creator as member
#         membership = GroupMember(group_id=new_group.id, user_id=session["user_id"])
#         db.session.add(membership)
#         db.session.commit()
        
#         return redirect(f"/group/{new_group.id}")
    
#     return render_template("create_group.html")


# @app.route("/group/<int:group_id>")
# def view_group(group_id):
#     if "user_id" not in session:
#         return redirect("/login")
    
#     group = Group.query.get_or_404(group_id)
    
#     # Check if user is member
#     is_member = GroupMember.query.filter_by(
#         group_id=group_id, 
#         user_id=session["user_id"]
#     ).first()
    
#     if not is_member:
#         return "You are not a member of this group", 403
    
#     # Get expenses
#     expenses = Expense.query.filter_by(group_id=group_id).order_by(Expense.created_at.desc()).all()
    
#     # Get members
#     members = GroupMember.query.filter_by(group_id=group_id).all()
    
#     return render_template("group.html", group=group, expenses=expenses, members=members)


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from models import db, User, Group, GroupMember, Expense, Debt


# TODO: take care of dates rendering in groups.html
# TODO: remove expenses only by the person who created it.


# Configure App
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize db with app
db.init_app(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show user's groups and recent expenses"""
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    # Get user's groups
    groups = db.execute("""
        SELECT g.id, g.name, g.theme, COUNT(DISTINCT gm.user_id) as member_count
        FROM groups g
        JOIN group_members gm ON g.id = gm.group_id
        WHERE g.id IN (
            SELECT group_id FROM group_members WHERE user_id = ?
        )
        GROUP BY g.id
        ORDER BY g.created_at DESC
    """, session["user_id"])
    username = user[0]["username"] if user else "User"
    return render_template("index.html", groups=groups, username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        flash(f"Welcome back, {rows[0]['username']}!")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    flash("Logged out successfully!")
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please provide username", 400)
        elif not password:
            return apology("Please provide password", 400)
        elif not confirmation:
            return apology("Please confirm password", 400)
        elif password != confirmation:
            return apology("Passwords do NOT match!", 400)
        try:
            result = db.execute("INSERT INTO users (username,hash) VALUES(?, ?)",
                                username, generate_password_hash(password))
            session["user_id"] = result
            flash(f"Welcome to Expense Splitter, {username}!")
            return redirect("/")
        except ValueError:
            return apology("username unavailable!", 400)

    return render_template("register.html")


@app.route("/create-group", methods=["GET", "POST"])
@login_required
def create_group():
    """Create a new group"""
    if request.method == "POST":
        name = request.form.get("name")
        theme = request.form.get("theme", "default")

        if not name:
            return apology("Please provide a group name", 400)

        # Create the group
        group_id = db.execute(
            "INSERT INTO groups (name, theme) VALUES(?, ?)",
            name, theme
        )

        # Add creator as first member
        db.execute(
            "INSERT INTO group_members (group_id, user_id) VALUES(?, ?)",
            group_id, session["user_id"]
        )

        flash(f"Group '{name}' created successfully! 🎊")
        return redirect(f"/group/{group_id}")

    else:
        return render_template("create_group.html")


@app.route("/group/<int:group_id>")
@login_required
def group(group_id):
    """Show group details and expenses"""

    # Verify user is a member of this group
    membership = db.execute("""
        SELECT * FROM group_members
        WHERE group_id = ? AND user_id = ?
    """, group_id, session["user_id"])

    if not membership:
        return apology("Why are you even here?", 403)

    # Get group info
    group = db.execute("SELECT * FROM groups WHERE id = ?", group_id)
    if not group:
        return apology("Group not found", 404)

    group = group[0]

    # Get group members
    members = db.execute("""
        SELECT u.id, u.username
        FROM users u
        JOIN group_members gm ON u.id = gm.user_id
        WHERE gm.group_id = ?
        ORDER BY gm.joined_at
    """, group_id)

    # Get expenses
    expenses = db.execute("""
        SELECT e.*, u.username as payer_name
        FROM expenses e
        JOIN users u ON e.paid_by = u.id
        WHERE e.group_id = ?
        ORDER BY e.created_at DESC
    """, group_id)

    return render_template("group.html", group=group, members=members, expenses=expenses)


@app.route("/group/<int:group_id>/add-expense", methods=["GET", "POST"])
@login_required
def add_expense(group_id):
    """Add expense to group"""

    # Verify user is a member
    membership = db.execute("""
        SELECT * FROM group_members
        WHERE group_id = ? AND user_id = ?
    """, group_id, session["user_id"])

    if not membership:
        return apology("You are not a member of this group", 403)

    if request.method == "POST":
        description = request.form.get("description")
        amount = request.form.get("amount")
        category = request.form.get("category", "💰")
        paid_by = request.form.get("paid_by")

        if not description:
            return apology("Please provide a description", 400)
        if not amount:
            return apology("Please provide an amount", 400)
        if not paid_by:
            return apology("Please select who paid", 400)

        try:
            amount = float(amount)
            if amount <= 0:
                return apology("Amount must be positive", 400)
        except ValueError:
            return apology("Invalid amount", 400)

        # Convert paid_by to int
        try:
            paid_by = int(paid_by)
        except ValueError:
            return apology("Invalid payer selection", 400)

        # Verify paid_by user is in the group
        payer_check = db.execute("""
            SELECT * FROM group_members
            WHERE group_id = ? AND user_id = ?
        """, group_id, paid_by)

        if not payer_check:
            return apology("Selected payer is not in this group", 400)

        # Add expense
        try:
            expense_id = db.execute("""
                INSERT INTO expenses (group_id, paid_by, amount, description, category)
                VALUES(?, ?, ?, ?, ?)
            """, group_id, paid_by, amount, description, category)

            print(f"✅ Expense created with ID: {expense_id}")

        except Exception as e:
            print(f"❌ Error creating expense: {e}")
            return apology(f"Error creating expense: {e}", 500)

        # Calculate split (equal split among all members)
        members = db.execute("""
            SELECT user_id FROM group_members WHERE group_id = ?
        """, group_id)

        if not members:
            return apology("No members found in group", 500)

        split_amount = amount / len(members)

        print(f"\n{'='*50}")
        print(f"DEBT CREATION DEBUG")
        print(f"{'='*50}")
        print(f"Expense ID: {expense_id}")
        print(f"Total Amount: ${amount:.2f}")
        print(f"Number of Members: {len(members)}")
        print(f"Split Amount: ${split_amount:.2f}")
        print(f"Paid by User ID: {paid_by}")
        print(f"All Members: {[m['user_id'] for m in members]}")
        print(f"{'='*50}\n")

        # Create debts for everyone except the payer
        debts_created = 0
        for member in members:
            member_id = member["user_id"]
            print(f"Checking member {member_id}...")

            if member_id != paid_by:
                print(f"  → Creating debt: User {member_id} owes User {paid_by} ${split_amount:.2f}")
                try:
                    debt_id = db.execute("""
                        INSERT INTO debts (expense_id, debtor_id, creditor_id, amount)
                        VALUES(?, ?, ?, ?)
                    """, expense_id, member_id, paid_by, split_amount)
                    print(f"  ✅ Debt created with ID: {debt_id}")
                    debts_created += 1
                except Exception as e:
                    print(f"  ❌ Error creating debt: {e}")
                    flash(f"Warning: Could not create debt for user {member_id}: {e}")
            else:
                print(f"  ⊘ Skipping (member is the payer)")

        print(f"\n{'='*50}")
        print(f"Total debts created: {debts_created}")
        print(f"{'='*50}\n")

        if debts_created == 0 and len(members) > 1:
            flash("Warning: No debts were created. This might indicate an issue.")

        flash(f"Expense '{description}' added successfully! 💸 ({debts_created} debts created)")
        return redirect(f"/group/{group_id}")

    else:
        # Get group members for the form
        members = db.execute("""
            SELECT u.id, u.username
            FROM users u
            JOIN group_members gm ON u.id = gm.user_id
            WHERE gm.group_id = ?
        """, group_id)

        group = db.execute("SELECT name FROM groups WHERE id = ?", group_id)[0]

        return render_template("add_expense.html", group_id=group_id, members=members, group=group)


@app.route("/group/<int:group_id>/add-member", methods=["GET", "POST"])
@login_required
def add_member(group_id):
    """Add members to the group"""
    membership = db.execute("""
        SELECT * FROM group_members
        WHERE group_id = ? AND user_id = ?
    """, group_id, session["user_id"])
    if not membership:
        return apology("Why are you here?", 403)
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Please provide username", 400)
        user = db.execute("SELECT id FROM users WHERE username = ?", username)
        if not user:
            return apology("User not found!", 404)
        user_id = user[0]["id"]
        existing = db.execute("""
                SELECT * FROM group_members
                WHERE group_id = ? AND user_id = ?
                """, group_id, user_id)
        if existing:
            return apology("User already in group!", 400)
        db.execute("""
            INSERT INTO group_members (group_id,user_id)
            VALUES(?, ?)
            """, group_id, user_id)
        flash(f"{username} added to the group!")
        return redirect(f"/group/{group_id}")
    else:
        group = db.execute("SELECT name FROM groups WHERE id = ?", group_id)[0]

        available_users = db.execute("""
            SELECT username FROM users
            WHERE id NOT IN (
                SELECT user_id FROM group_members WHERE group_id = ?
            )
            ORDER BY username
        """, group_id)

        return render_template("add_member.html", group_id=group_id,
                               group=group, available_users=available_users)
    return render_template("index.html")


@app.route("/balances")
@login_required
def balances():
    """Show user's debts and credits"""

    # Debts user owes
    owes = db.execute("""
        SELECT d.id, d.amount, u.username as creditor,
               e.description, e.category, d.created_at,
               g.name as group_name
        FROM debts d
        JOIN users u ON d.creditor_id = u.id
        JOIN expenses e ON d.expense_id = e.id
        JOIN groups g ON e.group_id = g.id
        WHERE d.debtor_id = ? AND d.paid = 0
        ORDER BY d.created_at DESC
    """, session["user_id"])

    # Debts owed to user
    owed = db.execute("""
        SELECT d.id, d.amount, u.username as debtor,
               e.description, e.category, d.created_at,
               g.name as group_name
        FROM debts d
        JOIN users u ON d.debtor_id = u.id
        JOIN expenses e ON d.expense_id = e.id
        JOIN groups g ON e.group_id = g.id
        WHERE d.creditor_id = ? AND d.paid = 0
        ORDER BY d.created_at DESC
    """, session["user_id"])

    total_owes = sum(debt["amount"] for debt in owes)
    total_owed = sum(debt["amount"] for debt in owed)

    return render_template("balances.html", owes=owes, owed=owed,
                           total_owes=total_owes, total_owed=total_owed)


@app.route("/mark-paid/<int:debt_id>", methods=["POST"])
@login_required
def mark_paid(debt_id):
    """Mark a debt as paid"""

    # Verify user is the creditor
    debt = db.execute("""
        SELECT * FROM debts WHERE id = ? AND creditor_id = ?
    """, debt_id, session["user_id"])

    if not debt:
        return apology("Debt not found or you're not authorized", 403)

    # Mark as paid
    db.execute("""
        UPDATE debts
        SET paid = 1, paid_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, debt_id)

    flash("Payment confirmed!")
    return redirect("/balances")


@app.route("/groups")
@login_required
def groups():
    groups = db.execute("""
            SELECT g.*
            FROM groups g
            JOIN group_members gm ON g.id = gm.group_id
            WHERE gm.user_id = ?
            ORDER BY g.created_at DESC
        """, session["user_id"])
    return render_template("groups.html", groups=groups)


if __name__ == "__main__":
    app.run(debug=True)
