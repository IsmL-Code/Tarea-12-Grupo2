# Nodo que representa una celda no vacía en la hoja de cálculo
class NodoCelda:
    def __init__(self, fila, columna, valor):
        self.fila = fila          # índice de fila de esta celda
        self.columna = columna    # índice de columna de esta celda
        self.valor = valor        # valor almacenado (no debe ser cero)
        self.siguiente = None     # puntero a la siguiente celda no vacía

class HojaCalculoDispersa:
    def __init__(self):
        self.celdas = None  # Lista enlazada simple de todas las celdas no vacías

    def insertar_actualizar(self, fila, columna, valor):
        
        #Inserta o actualiza el valor de la celda (fila, columna).
        #Si valor == 0, elimina la celda si existe.
        #Mantiene las celdas ordenadas por fila primero y luego columna.
        
        if valor == 0:
            self.eliminar(fila, columna)
            return

        nuevo = NodoCelda(fila, columna, valor)

        # Si la lista está vacía o debe ir al inicio
        if (not self.celdas or
            (fila < self.celdas.fila) or
            (fila == self.celdas.fila and columna < self.celdas.columna)):
            nuevo.siguiente = self.celdas
            self.celdas = nuevo
            return

        # Recorrer para encontrar la posición donde insertar o actualizar
        actual = self.celdas
        prev = None
        while (actual and
               ((actual.fila < fila) or
                (actual.fila == fila and actual.columna < columna))):
            prev = actual
            actual = actual.siguiente

        # Si ya existe una celda en esa posición, actualizar
        if actual and actual.fila == fila and actual.columna == columna:
            actual.valor = valor
        else:
            # insertar nuevo entre prev y actual
            nuevo.siguiente = actual
            prev.siguiente = nuevo

    def eliminar(self, fila, columna):
        
        #Elimina la celda en la posición (fila, columna) si existe.
        
        actual = self.celdas
        prev = None
        while actual:
            if actual.fila == fila and actual.columna == columna:
                if prev:
                    prev.siguiente = actual.siguiente
                else:
                    self.celdas = actual.siguiente
                return
            prev = actual
            actual = actual.siguiente

    def obtener_valor(self, fila, columna):
        
        #Devuelve el valor de la celda (fila, columna) si existe, sino 0.
       
        actual = self.celdas
        while actual:
            if actual.fila == fila and actual.columna == columna:
                return actual.valor
            actual = actual.siguiente
        return 0

    def sumar_rango(self, fila1, col1, fila2, col2):
        
        #Suma todos los valores de celdas no vacías cuyo (fila, columna)
        #esté dentro del rectángulo definido por fila1 ≤ fila ≤ fila2,
        #col1 ≤ columna ≤ col2.
        
        actual = self.celdas
        suma = 0
        while actual:
            if fila1 <= actual.fila <= fila2 and col1 <= actual.columna <= col2:
                suma += actual.valor
            actual = actual.siguiente
        return suma

    def promedio_rango(self, fila1, col1, fila2, col2):
       
        #Promedia los valores en el rango especificado.
        #Considera solo las celdas no vacías dentro del rango.
        
        actual = self.celdas
        suma = 0
        cuenta = 0
        while actual:
            if fila1 <= actual.fila <= fila2 and col1 <= actual.columna <= col2:
                suma += actual.valor
                cuenta += 1
            actual = actual.siguiente
        return (suma / cuenta) if cuenta > 0 else 0

    def eliminar_fila(self, fila):
        
        #Elimina todas las celdas que están en la fila dada.
        
        actual = self.celdas
        prev = None
        while actual:
            if actual.fila == fila:
                # eliminar este nodo
                if prev:
                    prev.siguiente = actual.siguiente
                    actual = prev.siguiente
                else:
                    self.celdas = actual.siguiente
                    actual = self.celdas
            else:
                prev = actual
                actual = actual.siguiente

    def eliminar_columna(self, columna):
        
        #Elimina todas las celdas que están en la columna dada.
        
        actual = self.celdas
        prev = None
        while actual:
            if actual.columna == columna:
                if prev:
                    prev.siguiente = actual.siguiente
                    actual = prev.siguiente
                else:
                    self.celdas = actual.siguiente
                    actual = self.celdas
            else:
                prev = actual
                actual = actual.siguiente

    def mostrar(self):
        
        #Muestra la hoja de cálculo en forma tabular.
        #Se calcula el rango de filas y columnas basándose en
        #las celdas no vacías para no recorrer espacio vacío innecesario.
        
        # Determinar máximos
        max_fila = 0
        max_col = 0
        actual = self.celdas
        while actual:
            if actual.fila > max_fila:
                max_fila = actual.fila
            if actual.columna > max_col:
                max_col = actual.columna
            actual = actual.siguiente

        # Mostrar encabezados de columnas
        header = "\t" + "\t".join(str(c) for c in range(1, max_col + 1))
        print(header)
        # Mostrar cada fila
        for f in range(1, max_fila + 1):
            fila_vals = []
            for c in range(1, max_col + 1):
                val = self.obtener_valor(f, c)
                fila_vals.append(str(val) if val != 0 else "")
            print(f"{f}:\t" + "\t".join(fila_vals))

    def guardar(self, archivo):
        
        #Guarda solo las celdas no vacías en un archivo.
        #Formato por línea: fila,columna,valor
        
        with open(archivo, "w") as f:
            actual = self.celdas
            while actual:
                f.write(f"{actual.fila},{actual.columna},{actual.valor}\n")
                actual = actual.siguiente

    def cargar(self, archivo):
        
        #Carga celdas desde un archivo guardado con el formato fila,columna,valor.
        #Limpia lo anterior.
        
        self.celdas = None
        try:
            with open(archivo, "r") as f:
                for linea in f:
                    fila, col, val = linea.strip().split(",")
                    self.insertar_actualizar(int(fila), int(col), float(val))
        except FileNotFoundError:
            print(f"Archivo no encontrado: {archivo}")


def hojacalculo():
    hoja = HojaCalculoDispersa()

    hoja.insertar_actualizar(1, 1, 10)
    hoja.insertar_actualizar(2, 3, 20)
    hoja.insertar_actualizar(3, 2, 30)
    hoja.insertar_actualizar(4, 4, 40)

    print("Mostrar hoja después de inserciones:")
    hoja.mostrar()

    print("\nObtener valor de (2,3):", hoja.obtener_valor(2, 3))
    print("Suma rango (1,1)-(3,3):", hoja.sumar_rango(1, 1, 3, 3))
    print("Promedio rango (1,1)-(4,4):", hoja.promedio_rango(1, 1, 4, 4))

    print("\nEliminar fila 2 y columna 4:")
    hoja.eliminar_fila(2)
    hoja.eliminar_columna(4)
    hoja.mostrar()

    hoja.guardar("hoja_calculo_Grupo_2.txt")
    print("\nCargando hoja desde archivo guardado:")
    hoja2 = HojaCalculoDispersa()
    hoja2.cargar("hoja_calculo_Grupo_2")
    hoja2.mostrar()

if __name__ == "__main__":
    hojacalculo()
