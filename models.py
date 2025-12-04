from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)
    
    # Relationships
    paid_expenses = db.relationship('Expense', backref='payer', lazy=True)
    debts_owed = db.relationship('Debt', foreign_keys='Debt.debtor_id', backref='debtor', lazy=True)
    debts_owed_to_me = db.relationship('Debt', foreign_keys='Debt.creditor_id', backref='creditor', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    theme = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    expenses = db.relationship('Expense', backref='group', lazy=True)
    members = db.relationship('GroupMember', backref='group', lazy=True)

    def __repr__(self):
        return f'<Group {self.name}>'


class GroupMember(db.Model):
    __tablename__ = 'group_members'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship to User
    user = db.relationship('User', backref='group_memberships')

    def __repr__(self):
        return f'<GroupMember user_id={self.user_id} group_id={self.group_id}>'


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    paid_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))  # 🍔 🚕 🎉 etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    debts = db.relationship('Debt', backref='expense', lazy=True)

    def __repr__(self):
        return f'<Expense {self.description} ${self.amount}>'


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

    def __repr__(self):
        return f'<Debt ${self.amount} paid={self.paid}>'