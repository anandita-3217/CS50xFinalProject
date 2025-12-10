from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)
    
    # Relationships
    groups = db.relationship('Group', secondary='group_members', back_populates='members')
    expenses_paid = db.relationship('Expense', back_populates='payer', foreign_keys='Expense.paid_by')
    debts_owed = db.relationship('Debt', back_populates='debtor', foreign_keys='Debt.debtor_id')
    debts_owed_to_me = db.relationship('Debt', back_populates='creditor', foreign_keys='Debt.creditor_id')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Group(db.Model):
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    theme = db.Column(db.String(50), default='default')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('User', secondary='group_members', back_populates='groups')
    expenses = db.relationship('Expense', back_populates='group', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Group {self.name}>'


class GroupMember(db.Model):
    __tablename__ = 'group_members'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('group_id', 'user_id', name='unique_group_user'),
    )
    
    def __repr__(self):
        return f'<GroupMember group={self.group_id} user={self.user_id}>'


class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    paid_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='default')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('Group', back_populates='expenses')
    payer = db.relationship('User', back_populates='expenses_paid', foreign_keys=[paid_by])
    debts = db.relationship('Debt', back_populates='expense', cascade='all, delete-orphan')
    splits = db.relationship('ExpenseSplit', back_populates='expense', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.CheckConstraint('amount > 0', name='check_amount_positive'),
    )
    
    def __repr__(self):
        return f'<Expense {self.description} ${self.amount}>'


class ExpenseSplit(db.Model):
    __tablename__ = 'expense_splits'
    
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    
    # Relationships
    expense = db.relationship('Expense', back_populates='splits')
    user = db.relationship('User')
    
    __table_args__ = (
        db.UniqueConstraint('expense_id', 'user_id', name='unique_expense_user'),
        db.CheckConstraint('amount >= 0', name='check_split_amount'),
    )
    
    def __repr__(self):
        return f'<ExpenseSplit expense={self.expense_id} user={self.user_id} ${self.amount}>'


class Debt(db.Model):
    __tablename__ = 'debts'
    
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id', ondelete='CASCADE'), nullable=False)
    debtor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creditor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)
    debtor_marked_paid = db.Column(db.Boolean, default=False)
    creditor_marked_paid = db.Column(db.Boolean, default=False)
    debtor_paid_at = db.Column(db.DateTime, nullable=True)
    creditor_paid_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    expense = db.relationship('Expense', back_populates='debts')
    debtor = db.relationship('User', back_populates='debts_owed', foreign_keys=[debtor_id])
    creditor = db.relationship('User', back_populates='debts_owed_to_me', foreign_keys=[creditor_id])
    
    __table_args__ = (
        db.CheckConstraint('amount > 0', name='check_debt_amount'),
        db.CheckConstraint('debtor_id != creditor_id', name='check_debtor_not_creditor'),
    )
    
    def __repr__(self):
        return f'<Debt debtor={self.debtor_id} creditor={self.creditor_id} ${self.amount}>'