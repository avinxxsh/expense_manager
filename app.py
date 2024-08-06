from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    recurring = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    expenses = Expense.query.all()
    total = sum(expense.amount for expense in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    description = request.form['description']
    amount = float(request.form['amount'])
    date = request.form['date']
    recurring = 'recurring' in request.form

    new_expense = Expense(description=description, amount=amount, date=date, recurring=recurring)
    db.session.add(new_expense)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/recurring_summary')
def recurring_summary():
    recurring_expenses = Expense.query.filter_by(recurring=True).all()
    total_recurring = sum(expense.amount for expense in recurring_expenses)
    return render_template('recurring_summary.html', recurring_expenses=recurring_expenses, total_recurring=total_recurring)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
