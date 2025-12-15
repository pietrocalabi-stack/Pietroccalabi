from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Inventory data
inventory = {}

@app.route('/')
def home():
    # Render the main page with the inventory data
    return render_template('index.html', inventory=inventory)

@app.route('/add', methods=['POST'])
def add_candy():
    # Add candy to the inventory
    date = request.form.get('date')
    candy_type = request.form.get('candy_type')
    quantity = int(request.form.get('quantity'))

    if date not in inventory:
        inventory[date] = {}
    if candy_type not in inventory[date]:
        inventory[date][candy_type] = 0
    inventory[date][candy_type] += quantity

    return redirect(url_for('home'))

@app.route('/remove', methods=['POST'])
def remove_candy():
    # Remove candy from the inventory
    date = request.form.get('date')
    candy_type = request.form.get('candy_type')
    quantity = int(request.form.get('quantity'))

    if date in inventory and candy_type in inventory[date]:
        inventory[date][candy_type] -= quantity
        if inventory[date][candy_type] <= 0:
            del inventory[date][candy_type]
        if not inventory[date]:
            del inventory[date]

    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    # Handle 404 errors with a custom message
    return "Page not found!", 404

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)