from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
import logging

# Configurar la carpeta de plantillas explícitamente
app = Flask(__name__, template_folder='templates')

# Configurar el registro de depuración
logging.basicConfig(level=logging.DEBUG)

# Inventory data
inventory = {}

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    # Render the main page with the inventory data
    logging.debug("Cargando la página principal con el inventario actual.")
    return render_template('index.html', inventory=inventory)

@app.route('/add', methods=['POST'])
def add_candy():
    # Add candy to the inventory
    date = request.form.get('date')
    category = request.form.get('category')
    item = request.form.get('item')
    quantity = int(request.form.get('quantity'))

    logging.debug(f"Añadiendo: date={date}, category={category}, item={item}, quantity={quantity}")

    if date not in inventory:
        inventory[date] = {}
    if category not in inventory[date]:
        inventory[date][category] = {}
    if item not in inventory[date][category]:
        inventory[date][category][item] = 0
    inventory[date][category][item] += quantity

    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete_candy():
    # Delete candy from the inventory
    date = request.form.get('date')
    category = request.form.get('category')
    item = request.form.get('item')

    logging.debug(f"Intentando eliminar: date={date}, category={category}, item={item}")

    if date in inventory and category in inventory[date] and item in inventory[date][category]:
        del inventory[date][category][item]
        logging.debug(f"Elemento eliminado: {item} de la categoría {category} en la fecha {date}")
        if not inventory[date][category]:
            del inventory[date][category]
            logging.debug(f"Categoría eliminada: {category} en la fecha {date}")
        if not inventory[date]:
            del inventory[date]
            logging.debug(f"Fecha eliminada: {date}")
    else:
        logging.warning("No se encontró el elemento para eliminar. Verifica los datos enviados.")

    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    # Handle 404 errors with a custom message
    logging.error("Error 404: Página no encontrada.")
    return "Page not found!", 404

if __name__ == '__main__':
    # Run the Flask app in debug mode
    logging.info("Iniciando la aplicación Flask en modo debug.")
    app.run(debug=True)