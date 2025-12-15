PROYECTO FINAL: Inventario

Uso rápido:
- Escribe el ítem y sus especificaciones (marca, tipo) y el precio (Bs).
- Ajusta la cantidad con los botones “＋/−”.
- Al agregar, el ítem aparece en la tabla con el subtotal (precio × cantidad).

Cómo ejecutar:
- Candy Inventory:
	- python "c:\Users\pietr\Documents\Proyectofinal\candy_inventory\main.py"
- Inventory Management:
	- python "c:\Users\pietr\Documents\Proyectofinal\inventory_management\main.py"
- Abre http://localhost:5000

Fotos:
- En `inventory_management` puedes subir/tomar una foto del ítem; se guarda en `inventory_management/static/uploads` y se muestra como miniatura.

Git (organizar commits):
- Detén los servidores Flask antes de confirmar (CTRL+C).
- Commit UI candy:
	- git -C "c:\Users\pietr\Documents\Proyectofinal" add candy_inventory/templates/index.html
	- git -C "c:\Users\pietr\Documents\Proyectofinal" commit -m "style(candy_inventory): UI moderno, Bs y controles de cantidad"
- Commit inventory_management:
	- git -C "c:\Users\pietr\Documents\Proyectofinal" add inventory_management/main.py inventory_management/static/uploads
	- git -C "c:\Users\pietr\Documents\Proyectofinal" commit -m "feat(inventory_management): fotos de ítems, subtotal en Bs, tema moderno"
- Commit documentación:
	- git -C "c:\Users\pietr\Documents\Proyectofinal" add README.md
	- git -C "c:\Users\pietr\Documents\Proyectofinal" commit -m "docs: guía de ejecución y flujo de commits"

Siguiente paso recomendado:
- Persistencia (SQLite/SQLAlchemy) para no perder datos al reiniciar y permitir edición/eliminación por fila.