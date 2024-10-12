from flask import Flask, render_template, redirect, url_for, flash, request
app = Flask (__name__)
app.secret_key="delunoalnueve"
 

#04 🛒 Grocery
# Diseña un programa de lista de compras que pueda:
# - Crear una nueva lista de compras
# - Agregar items con sus cantidades
# - Eliminar items de la lista
# - Mostrar la lista completa
# - Calcular el costo total de la lista basado en precios predefinidos
# - Guardar y cargar listas de compras desde un archivo


class Grocery:
    def __init__(self):
        #                  dicc  { str            list      }
        self.items = {}  #items= {nombre : (cantidad, precio)}

    def add(self, nombre, cant, price):
        if nombre in self.items:
            maybecosa, maybeprecio = self.items[nombre]
            self.items[nombre] = (maybecosa + cant, price)
        else:
            self.items[nombre] = (cant, price)
        print(f"Agregado: {cant} {nombre}(s) a ${price:.2f} cada uno")

    def show(self):
        if not self.items:
            print("¡Aún no tienes nada en tu papu lista!")
        else:
            print("\nLista de compras:")
            for nombre, (cant, price) in self.items.items():
                print(f"\t{nombre}: {cant} a ${price:.2f} cada uno")


    def delete(self, nombre):
        if nombre in self.items:
            del self.items[nombre]
            print(f"{nombre} ha sido borrado con éxito.")
        else:
            print(f"{nombre} no está en la lista.")


    def pagar(self):
        total = 0
        for nombre, (cant, price) in self.items.items():
            total += cant * price
        return total


    def save(self, archivo):
        with open(archivo, 'w') as f:
            for nombre, (cant, price) in self.items.items():
                f.write(f"{nombre},{cant},{price}\n")
        print("Lista de compras guardada.")


    def load(self, archivo):
        try:
            with open(archivo, 'r') as f:
                self.items = {}
                for linea in f:
                    nombre, cant, price = linea.strip().split(",")
                    self.items[nombre] = (int(cant), float(price))
            print("Lista de compras cargada.")
        except FileNotFoundError:
            print("Error al buscar el archivo.")
        except ValueError:
            print("Error al leer el archivo.")



lista = Grocery()

@app.route("/")
def index():
    return render_template("inicio.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        nombre = request.form["nombre"]
        cant = int(request.form["cant"])
        price = float(request.form["price"])
        lista.add(nombre, cant, price)
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/show")
def show():
    return render_template("show.html", items=lista.items)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        nombre = request.form["nombre"]
        lista.delete(nombre)
        return redirect(url_for("index"))
    return render_template("delete.html")


@app.route("/pagar")
def pagar():
    total = lista.pagar()
    return render_template("pagar.html", total=total)


@app.route("/save", methods=["GET", "POST"])
def save():
    if request.method == "POST":
        archivo = request.form["archivo"]
        lista.save(archivo)
        return redirect(url_for("index"))
    return render_template("save.html")


@app.route("/load", methods=["GET", "POST"])
def load():
    if request.method == "POST":
        archivo = request.form["archivo"]
        lista.load(archivo)
        return redirect(url_for("index"))
    return render_template("load.html")

if __name__ == "__main__":
    app.run(debug=True)