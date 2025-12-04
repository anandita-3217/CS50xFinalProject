from  flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db =SQLAlchemy()
class User:
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80),unique= True,nullable=False)
    hash = db.Column(db.String(200), nullable =False)
    paid_expenses = db.relationship('Expense', backref='payer', lazy=True)
    debts_owed = db.relationship('Debt', foreign_keys='Debt.debtor_id', backref='debtor', lazy=True)
    debts_owed_to_me = db.relationship('Debt', foreign_keys='Debt.creditor_id', backref='creditor', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)
    
    # Relationships
    paid_expenses = db.relationship('Expense', backref='payer', lazy=True)
    debts_owed = db.relationship('Debt', foreign_keys='Debt.debtor_id', backref='debtor', lazy=True)
    debts_owed_to_me = db.relationship('Debt', foreign_keys='Debt.creditor_id', backref='creditor', lazy=True)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    theme = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    expenses = db.relationship('Expense', backref='group', lazy=True)
    members = db.relationship('GroupMember', backref='group', lazy=True)

class GroupMember(db.Model):
    __tablename__ = 'group_members'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship to User
    user = db.relationship('User', backref='group_memberships')

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    paid_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))  # emoji category
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    debts = db.relationship('Debt', backref='expense', lazy=True)

class Debt(db.Model):
    __tablename__ = 'debts'
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'), nullable=False)
    debtor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creditor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

# Routes
