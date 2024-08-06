from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

expenses = []

@app.route('/')
def index():
    total = sum(float(expense['amount']) for expense in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods = ['POST'])
def add_expense():
    description = request.form.get('description')
    amount = request.form.get('amount')
    date = request.form.get('date')

    if description and amount and date:
        expenses.append({'description': description, 'amount': amount, 'date': date})
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)