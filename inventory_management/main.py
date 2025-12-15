from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Inventory as a list of entries
inventory = []

# HTML template as a string
template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestión de Inventario</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
        }
        header {
            background-color: #ff6f61;
            color: white;
            padding: 1rem;
            text-align: center;
        }
        .container {
            padding: 2rem;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 0.5rem;
            text-align: center;
        }
        th {
            background-color: #ff6f61;
            color: white;
        }
        form {
            margin-top: 1rem;
        }
        form input, form button {
            padding: 0.5rem;
            margin: 0.5rem 0;
        }
        .qty-control {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        .qty-btn {
            background-color: #ff6f61;
            color: #fff;
            border: none;
            padding: 0.4rem 0.6rem;
            border-radius: 4px;
            cursor: pointer;
        }
        .qty-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
    </style>
    <script>
        function setupQtyControls() {
            const minus = document.getElementById('qty-minus');
            const plus = document.getElementById('qty-plus');
            const input = document.querySelector('input[name="quantity"]');

            function clamp(val) {
                const n = Math.max(1, Math.floor(val));
                return n;
            }

            minus.addEventListener('click', (e) => {
                e.preventDefault();
                input.value = clamp((parseInt(input.value || '1', 10) - 1));
            });

            plus.addEventListener('click', (e) => {
                e.preventDefault();
                input.value = clamp((parseInt(input.value || '1', 10) + 1));
            });
        }

        document.addEventListener('DOMContentLoaded', setupQtyControls);
    </script>
</head>
<body>
    <header>
        <h1>Gestión de Inventario</h1>
    </header>
    <div class="container">
        <h2>Inventario</h2>
        <table>
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Categoría</th>
                    <th>Ítem</th>
                    <th>Cantidad</th>
                    <th>Precio (Bs)</th>
                    <th>Subtotal (Bs)</th>
                </tr>
            </thead>
            <tbody>
                {% for entry in inventory %}
                    <tr>
                        <td>{{ entry.date }}</td>
                        <td>{{ entry.category }}</td>
                        <td>{{ entry.item }}</td>
                        <td>{{ entry.quantity }}</td>
                        <td>Bs {{ '%.2f' % entry.price }}</td>
                        <td>Bs {{ '%.2f' % (entry.price * entry.quantity) }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>

        <h2>Agregar Ítems</h2>
        <form action="/add" method="POST">
            <input type="date" name="date" required>

            <div>
                <strong>Seleccionar Ítem</strong><br>
                <label><input type="radio" name="item" value="Arcor" required> Arcor (Chocolate)</label><br>
                <label><input type="radio" name="item" value="El Ceibo"> El Ceibo (Chocolate)</label><br>
                <label><input type="radio" name="item" value="Condor"> Condor (Chocolate)</label><br>
                <label><input type="radio" name="item" value="Para Ti"> Para Ti (Chocolate)</label><br>
                <label><input type="radio" name="item" value="Breick"> Breick (Chocolate)</label><br>
                <label><input type="radio" name="item" value="Groso"> Groso (Chicle)</label><br>
                <label><input type="radio" name="item" value="Chiclets"> Chiclets (Chicle)</label><br>
                <label><input type="radio" name="item" value="Trident"> Trident (Chicle)</label><br>
                <label><input type="radio" name="item" value="Beldent"> Beldent (Chicle)</label><br>
                <label><input type="radio" name="item" value="Mogul"> Mogul (Gomita)</label><br>
                <label><input type="radio" name="item" value="Fini"> Fini (Gomita)</label><br>
                <label><input type="radio" name="item" value="Alka"> Alka (Caramelo)</label><br>
                <label><input type="radio" name="item" value="Fizz"> Fizz (Caramelo)</label><br>
                <label><input type="radio" name="item" value="Halls"> Halls (Caramelo)</label><br>
                <label><input type="radio" name="item" value="Chocomenta"> Chocomenta (Caramelo)</label><br>
                <label><input type="radio" name="item" value="Butter Toffes"> Butter Toffes (Caramelo)</label><br>
                <label><input type="radio" name="item" value="Sparkies"> Sparkies (Caramelo)</label>
            </div>

            <input type="number" name="price" placeholder="Precio (Bs)" min="0" step="0.01" required>

            <div class="qty-control">
                <button id="qty-minus" class="qty-btn">-</button>
                <input type="number" name="quantity" min="1" value="1" required>
                <button id="qty-plus" class="qty-btn">+</button>
            </div>

            <button type="submit">Agregar</button>
        </form>
    </div>
</body>
</html>"""

@app.route('/')
def home():
    # Render the main page with the inventory data
    return render_template_string(template, inventory=inventory)

@app.route('/add', methods=['POST'])
def add_item():
    # Add item to the inventory
    date = request.form.get('date')
    item = request.form.get('item')
    quantity_raw = request.form.get('quantity')
    price_raw = request.form.get('price')

    # Derive category from item selection
    if item in ["Arcor", "El Ceibo", "Condor", "Para Ti", "Breick"]:
        category = "Chocolates"
    elif item in ["Groso", "Chiclets", "Trident", "Beldent"]:
        category = "Chicles"
    elif item in ["Mogul", "Fini"]:
        category = "Gomitas"
    elif item in ["Alka", "Fizz", "Halls", "Chocomenta", "Butter Toffes", "Sparkies"]:
        category = "Caramelos"
    else:
        category = "Otros"

    try:
        quantity = int(quantity_raw)
    except (TypeError, ValueError):
        quantity = 1

    try:
        price = float(price_raw)
    except (TypeError, ValueError):
        price = 0.0

    entry = {
        'date': date,
        'category': category,
        'item': item,
        'quantity': quantity,
        'price': price,
    }
    inventory.append(entry)

    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    # Handle 404 errors with a custom message
    return "Page not found!", 404

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)