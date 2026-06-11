from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

BUDGET_LIMIT = 10000  # set your monthly spending limit

@app.route("/")
def expenses():
    return render_template("expenses.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    months = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]

    if request.method == "POST":
        select_month = request.form.get("month")
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        description = request.form.get("description")

        # Save expense to file
        with open("Expenses.txt", "a") as f:
            f.write(f"Month: {select_month}, Amount: {amount}, Category: {category}, Description: {description}, Date: {datetime.now()}\n")

        # Here we checked total spending
        total = 0
        with open("Expenses.txt", "r") as f:
            for line in f:
                if "Amount:" in line:
                    amnt = float(line.split("Amount:")[1].split(",")[0].strip())
                    total += amnt

        # We checked if budget hitted the limit!
        if total > BUDGET_LIMIT:
            return f"<h2 style='color:red;'> Budget Limit Crossed!</h2><p>Total Spent: ₹{total} / ₹{BUDGET_LIMIT}</p><a href='/add'>Back</a>"
        else:
            return f"<h2>✅ Expense Added Successfully!</h2><p>Month: {select_month} | Amount: ₹{amount} | Category: {category} | {description}</p><p>Total Spent: ₹{total} / ₹{BUDGET_LIMIT}</p><a href='/add'>Add Another</a>"
            
        
     

    return render_template("add.html", months=months)

if __name__ == "__main__":
    app.run(debug=True)
