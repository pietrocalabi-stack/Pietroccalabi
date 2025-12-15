from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Inventory data: list of entries with details
inventory = []

@app.route('/')
def home():
    return render_template('index.html', inventory=inventory)

@app.route('/add', methods=['POST'])
def add_item():
    date = request.form.get('date')
    name = request.form.get('name')
    brand = request.form.get('brand')
    item_type = request.form.get('type')
    price_raw = request.form.get('price')
    quantity_raw = request.form.get('quantity')

    try:
        price = float(price_raw)
    except (TypeError, ValueError):
        price = 0.0

    try:
        quantity = int(quantity_raw)
    except (TypeError, ValueError):
        quantity = 0

    entry = {
        'date': date,
        'name': name,
        'brand': brand,
        'type': item_type,
        'price': price,
        'quantity': quantity,
    }
    inventory.append(entry)

    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete_item():
    idx_raw = request.form.get('idx')
    try:
        idx = int(idx_raw)
        if 0 <= idx < len(inventory):
            inventory.pop(idx)
    except (TypeError, ValueError):
        pass

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)