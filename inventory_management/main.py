from flask import Flask, render_template_string, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

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
        :root{
            --bg: #0f172a;            /* slate-900 */
            --card: #0b1020;         /* darker card */
            --muted: #94a3b8;        /* slate-400 */
            --text: #e5e7eb;         /* slate-200 */
            --primary: #7c3aed;      /* violet-600 */
            --primary-hover: #6d28d9;/* violet-700 */
            --accent: #22d3ee;       /* cyan-400 */
            --border: #1f2937;       /* slate-800 */
            --success: #10b981;      /* emerald-500 */
        }
        *{box-sizing:border-box}
        body {
            font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: var(--text);
            background: radial-gradient(1200px 600px at 10% -10%, rgba(124,58,237,0.20), transparent),
                        radial-gradient(1200px 600px at 90% 110%, rgba(34,211,238,0.20), transparent),
                        var(--bg);
        }
        header {
            position: sticky;
            top: 0;
            background: linear-gradient(90deg, rgba(124,58,237,0.25), rgba(34,211,238,0.20));
            border-bottom: 1px solid var(--border);
            backdrop-filter: blur(6px);
            padding: 1rem 2rem;
        }
        .brand {
            display:flex; align-items:center; gap:.75rem; justify-content:center;
            font-weight: 700; letter-spacing:.3px;
        }
        .brand .dot{width:10px; height:10px; border-radius:50%; background:var(--accent)}
        .container {
            padding: 2rem;
            max-width: 1050px;
            margin: 0 auto;
        }
        .grid{display:grid; grid-template-columns: 1fr 1fr; gap: 1.25rem}
        .card {
            background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.00));
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.25rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.25);
        }
        .card h2 {margin:0 0 .75rem 0; font-size:1.1rem; color:var(--muted)}
        table {
            width: 100%;
            border-collapse: collapse;
            background: transparent;
        }
        th, td {
            padding: 0.75rem;
            text-align: center;
            border-bottom: 1px solid var(--border);
        }
        thead th {
            font-weight:600; color:var(--muted);
            background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.00));
        }
        tbody tr:hover {background: rgba(124,58,237,0.06)}
        .thumb {
            width: 56px; height: 56px; object-fit: cover;
            border-radius: 8px; border: 1px solid var(--border);
            box-shadow: 0 8px 16px rgba(124,58,237,0.25);
        }
        .row {display:flex; gap:.75rem}
        .input, select, input[type="number"], input[type="date"], input[type="file"]{
            width: 100%; background: var(--card); color:var(--text);
            border:1px solid var(--border); border-radius:8px;
            padding:.6rem .75rem; outline:none;
        }
        .input:focus, select:focus, input[type="number"]:focus, input[type="date"]:focus {border-color: var(--accent)}
        .qty-control { display:inline-flex; align-items:center; gap:.5rem }
        .qty-btn {
            background: var(--primary); color:#fff; border:none;
            padding:.5rem .7rem; border-radius:8px; cursor:pointer;
            transition: transform .08s ease, background .15s ease;
        }
        .qty-btn:hover { background: var(--primary-hover); transform: translateY(-1px) }
        .btn {
            background: linear-gradient(90deg, var(--primary), var(--accent));
            color:#0b1020; font-weight:700;
            border:none; padding:.7rem 1rem; border-radius:10px; cursor:pointer;
            box-shadow: 0 14px 28px rgba(124,58,237,0.35);
        }
        .btn:hover{filter: brightness(1.05)}
        .hint{color:var(--muted); font-size:.85rem}
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
        <div class="grid">
        <div class="card">
        <h2>Inventario</h2>
        <table>
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Categoría</th>
                    <th>Ítem</th>
                    <th>Foto</th>
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
                        <td>
                            {% if entry.photo_url %}
                                <img class="thumb" src="{{ entry.photo_url }}" alt="foto">
                            {% else %}
                                —
                            {% endif %}
                        </td>
                        <td>{{ entry.quantity }}</td>
                        <td>Bs {{ '%.2f' % entry.price }}</td>
                        <td>Bs {{ '%.2f' % (entry.price * entry.quantity) }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
        </div>

        <div class="card">
        <h2>Agregar Ítems</h2>
        <form action="/add" method="POST" enctype="multipart/form-data">
            <div class="row">
                <input class="input" type="date" name="date" required>
                <input class="input" type="number" name="price" placeholder="Precio (Bs)" min="0" step="0.01" required>
            </div>

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

            <label class="hint">Foto del ítem (puedes tomarla)
                <input class="input" type="file" name="photo" accept="image/*" capture="environment">
            </label>

            <div class="qty-control">
                <button id="qty-minus" class="qty-btn">−</button>
                <input class="input" type="number" name="quantity" min="1" value="1" required>
                <button id="qty-plus" class="qty-btn">＋</button>
            </div>

            <button class="btn" type="submit">Agregar</button>
        </form>
        </div>
        </div>
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
    photo = request.files.get('photo')

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

    photo_url = None
    if photo and photo.filename:
        name, ext = os.path.splitext(photo.filename)
        if ext.lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(f"{item}_{date}{ext.lower()}")
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                photo.save(save_path)
                photo_url = url_for('static', filename=f'uploads/{filename}')
            except Exception:
                photo_url = None

    entry = {
        'date': date,
        'category': category,
        'item': item,
        'quantity': quantity,
        'price': price,
        'photo_url': photo_url,
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