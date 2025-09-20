#definimos una clase que representa una línea de texto en el editor (nodo de una lista enlazada)
class NodoLinea:
    def __init__(self, texto):
        self.texto = texto  # Contenido de la línea
        self.siguiente = None  # Referencia a la siguiente línea

# Clase que simula un editor de texto basado en una lista enlazada
class EditorTexto:
    def __init__(self):
        self.cabeza = None  # Inicio del documento (primera línea)
        self.tamaño = 0     # Número de líneas en el documento

    def insertar_linea(self, posicion, texto):
        # Inserta una línea en la posición indicada
        nuevo = NodoLinea(texto)
        if posicion < 1:
            print("Posición inválida")
            return
        if posicion == 1:
            # Insertar al principio
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            prev = None
            i = 1
            while actual and i < posicion:
                prev = actual
                actual = actual.siguiente
                i += 1
            if i == posicion:
                # Insertar en el medio
                prev.siguiente = nuevo
                nuevo.siguiente = actual
            else:
                # Posición mayor al tamaño + 1, se inserta al final
                if prev:
                    prev.siguiente = nuevo
                else:
                    self.cabeza = nuevo
        self.tamaño += 1

    def eliminar_linea(self, posicion):
        # Elimina la línea en la posición indicada
        if posicion < 1 or not self.cabeza:
            print("Posición inválida o lista vacía")
            return
        if posicion == 1:
            self.cabeza = self.cabeza.siguiente
            self.tamaño -= 1
            return
        actual = self.cabeza
        prev = None
        i = 1
        while actual and i < posicion:
            prev = actual
            actual = actual.siguiente
            i += 1
        if actual:
            prev.siguiente = actual.siguiente
            self.tamaño -= 1
        else:
            print("Posición fuera de rango")

    def mover_linea(self, origen, destino):
        # Mueve una línea desde 'origen' hasta la posición 'destino'
        if origen == destino or origen < 1 or destino < 1 or origen > self.tamaño or destino > self.tamaño:
            print("Posiciones inválidas para mover")
            return

        # Extraer la línea de origen
        prev = None
        actual = self.cabeza
        i = 1
        while actual and i < origen:
            prev = actual
            actual = actual.siguiente
            i += 1
        if not actual:
            print("Origen fuera de rango")
            return

        # Remover nodo de su posición original
        if prev:
            prev.siguiente = actual.siguiente
        else:
            self.cabeza = actual.siguiente

        # Insertar en la nueva posición
        if destino == 1:
            actual.siguiente = self.cabeza
            self.cabeza = actual
        else:
            prev2 = None
            actual2 = self.cabeza
            j = 1
            while actual2 and j < destino:
                prev2 = actual2
                actual2 = actual2.siguiente
                j += 1
            prev2.siguiente = actual
            actual.siguiente = actual2

    def buscar_texto(self, texto):
        # Busca todas las líneas que contengan el texto dado
        actual = self.cabeza
        lineas = []
        pos = 1
        while actual:
            if texto in actual.texto:
                lineas.append((pos, actual.texto))
            actual = actual.siguiente
            pos += 1
        return lineas

    def reemplazar_texto(self, linea_num, texto_nuevo):
        # Reemplaza el contenido de una línea específica
        if linea_num < 1 or linea_num > self.tamaño:
            print("Número de línea inválido")
            return
        actual = self.cabeza
        i = 1
        while actual and i < linea_num:
            actual = actual.siguiente
            i += 1
        if actual:
            actual.texto = texto_nuevo

    def mostrar(self):
        # Muestra todas las líneas del documento
        actual = self.cabeza
        i = 1
        print("Contenido del editor:")
        while actual:
            print(f"{i}: {actual.texto}")
            actual = actual.siguiente
            i += 1

    def guardar_archivo(self, nombre_archivo):
        # Guarda el contenido del documento en un archivo de texto
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            actual = self.cabeza
            while actual:
                f.write(actual.texto + "\n")
                actual = actual.siguiente

    def cargar_archivo(self, nombre_archivo):
        # Carga el contenido de un archivo de texto en el editor
        self.cabeza = None
        self.tamaño = 0
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    self.insertar_linea(self.tamaño + 1, linea.rstrip("\n"))
        except FileNotFoundError:
            print(f"No se encontró el archivo: {nombre_archivo}")

# Función que demuestra cómo funciona el editor
def editor_textos():
    editor = EditorTexto()

    # Insertar líneas
    editor.insertar_linea(1, "hola somos el grupo 2")
    editor.insertar_linea(2, "estamosen el dipolmado de tics")
    editor.insertar_linea(3, "y estamos aprendiendo python")
    editor.mostrar()

    # Insertar en el medio
    print("\nInsertar línea en posición 2")
    editor.insertar_linea(2, "Nueva línea en medio")
    editor.mostrar()

    # Eliminar una línea
    print("\nEliminar línea 3")
    editor.eliminar_linea(3)
    editor.mostrar()

    # Mover línea 3 al inicio
    print("\nMover línea 3 a la posición 1")
    editor.mover_linea(3, 1)
    editor.mostrar()

    # Buscar texto
    print("\nBuscar texto 'línea'")
    resultados = editor.buscar_texto("línea")
    for pos, texto in resultados:
        print(f"Encontrado en línea {pos}: {texto}")

    # Reemplazar texto
    print("\nReemplazar texto en línea 2")
    editor.reemplazar_texto(2, "Texto reemplazado")
    editor.mostrar()

    # Guardar archivo
    print("\nGuardar a archivo 'ejemplo.txt'")
    editor.guardar_archivo("ejemplo.txt")

    # Limpiar y cargar desde archivo
    print("\nLimpiar editor y cargar desde archivo 'ejemplo.txt'")
    editor.cabeza = None
    editor.tamaño = 0
    editor.cargar_archivo("ejemplo.txt")
    editor.mostrar()


if __name__ == "__main__":
    editor_textos()
