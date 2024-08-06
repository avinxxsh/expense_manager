from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

expenses = []

@app.route('/')
def index():
    total = sum(float(expense['amount']) for expense in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add_expense():
    description = request.form.get('description')
    amount = request.form.get('amount')
    date = request.form.get('date')
    recurring = 'recurring' in request.form  # Check if the recurring checkbox was checked

    if description and amount and date:
        expenses.append({'description': description, 'amount': amount, 'date': date, 'recurring': recurring})

    return redirect(url_for('index'))

@app.route('/recurring')
def recurring_summary():
    total_recurring = sum(float(expense['amount']) for expense in expenses if expense['recurring'])
    recurring_expenses = [expense for expense in expenses if expense['recurring']]
    return render_template('recurring_summary.html', total_recurring=total_recurring, recurring_expenses=recurring_expenses)


if __name__ == '__main__':
    app.run(debug=True)