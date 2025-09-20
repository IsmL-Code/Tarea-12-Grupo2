# definimos que representa un término de un polinomio (nodo de una lista enlazada)
class NodoTermino:
    def __init__(self, coef, exp):
        self.coef = coef  # Coeficiente del término (por ejemplo: 3 en 3x^2)
        self.exp = exp    # Exponente del término (por ejemplo: 2 en 3x^2)
        self.siguiente = None  # Referencia al siguiente término

# Clase que representa un polinomio como lista enlazada de términos ordenados por exponente
class Polinomio:
    def __init__(self):
        self.cabeza = None  # Inicio del polinomio

    def insertar_termino(self, coef, exp):
        # Inserta un término en orden descendente por exponente
        if coef == 0:
            return  # No se insertan términos con coeficiente 0

        nuevo = NodoTermino(coef, exp)

        # Caso 1: insertar al principio
        if not self.cabeza or exp > self.cabeza.exp:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            prev = None

            # Buscar posición correcta para insertar
            while actual and actual.exp > exp:
                prev = actual
                actual = actual.siguiente

            if actual and actual.exp == exp:
                # Ya existe un término con mismo exponente → se suman los coeficientes
                actual.coef += coef

                # Si el coeficiente resultante es 0, se elimina el nodo
                if actual.coef == 0:
                    if prev:
                        prev.siguiente = actual.siguiente
                    else:
                        self.cabeza = actual.siguiente
            else:
                # Insertar nuevo nodo en medio o al final
                nuevo.siguiente = actual
                if prev:
                    prev.siguiente = nuevo
                else:
                    self.cabeza = nuevo

    def mostrar(self):
        # Muestra el polinomio en notación matemática estándar
        actual = self.cabeza
        if not actual:
            print("0")
            return
        resultado = ""
        while actual:
            c = actual.coef
            e = actual.exp
            signo = "+" if c > 0 else "-"
            c_abs = abs(c)

            if resultado == "":
                signo = "" if c > 0 else "-"

            if e == 0:
                resultado += f"{signo}{c_abs}"
            elif e == 1:
                if c_abs == 1:
                    resultado += f"{signo}x"
                else:
                    resultado += f"{signo}{c_abs}x"
            else:
                if c_abs == 1:
                    resultado += f"{signo}x^{e}"
                else:
                    resultado += f"{signo}{c_abs}x^{e}"
            actual = actual.siguiente
        print(resultado)

    def sumar(self, otro):
        # Devuelve un nuevo polinomio que es la suma de self + otro
        resultado = Polinomio()

        actual = self.cabeza
        while actual:
            resultado.insertar_termino(actual.coef, actual.exp)
            actual = actual.siguiente

        actual = otro.cabeza
        while actual:
            resultado.insertar_termino(actual.coef, actual.exp)
            actual = actual.siguiente

        return resultado

    def restar(self, otro):
        # Devuelve un nuevo polinomio que es la resta de self - otro
        resultado = Polinomio()

        actual = self.cabeza
        while actual:
            resultado.insertar_termino(actual.coef, actual.exp)
            actual = actual.siguiente

        actual = otro.cabeza
        while actual:
            resultado.insertar_termino(-actual.coef, actual.exp)
            actual = actual.siguiente

        return resultado

    def multiplicar(self, otro):
        # Devuelve un nuevo polinomio que es el producto de self * otro
        resultado = Polinomio()

        actual1 = self.cabeza
        while actual1:
            actual2 = otro.cabeza
            while actual2:
                coef_prod = actual1.coef * actual2.coef
                exp_sum = actual1.exp + actual2.exp
                resultado.insertar_termino(coef_prod, exp_sum)
                actual2 = actual2.siguiente
            actual1 = actual1.siguiente

        return resultado

    def evaluar(self, x):
        # Evalúa el polinomio para un valor dado de x
        actual = self.cabeza
        resultado = 0
        while actual:
            resultado += actual.coef * (x ** actual.exp)
            actual = actual.siguiente
        return resultado

    def derivar(self):
        # Devuelve la derivada del polinomio
        resultado = Polinomio()
        actual = self.cabeza
        while actual:
            if actual.exp != 0:
                nuevo_coef = actual.coef * actual.exp
                nuevo_exp = actual.exp - 1
                resultado.insertar_termino(nuevo_coef, nuevo_exp)
            actual = actual.siguiente
        return resultado

    def integrar(self):
        # Devuelve la integral indefinida del polinomio (sin constante de integración)
        resultado = Polinomio()
        actual = self.cabeza
        while actual:
            nuevo_coef = actual.coef / (actual.exp + 1)
            nuevo_exp = actual.exp + 1
            resultado.insertar_termino(nuevo_coef, nuevo_exp)
            actual = actual.siguiente
        return resultado

# Función de demostración
def sistema_polinomios():
    p1 = Polinomio()
    p1.insertar_termino(3, 4)     # 3x^4
    p1.insertar_termino(-2, 2)    # -2x^2
    p1.insertar_termino(5, 0)     # +5
    print("Polinomio p1:")
    p1.mostrar()

    p2 = Polinomio()
    p2.insertar_termino(1, 3)     # x^3
    p2.insertar_termino(4, 2)     # 4x^2
    p2.insertar_termino(-5, 0)    # -5
    print("Polinomio p2:")
    p2.mostrar()

    print("Suma p1 + p2:")
    suma = p1.sumar(p2)
    suma.mostrar()

    print("Resta p1 - p2:")
    resta = p1.restar(p2)
    resta.mostrar()

    print("Multiplicación p1 * p2:")
    mult = p1.multiplicar(p2)
    mult.mostrar()

    x = 2
    print(f"Evaluar p1 en x={x}: {p1.evaluar(x)}")

    print("Derivar p1:")
    deriv = p1.derivar()
    deriv.mostrar()

    print("Integrar p1:")
    integ = p1.integrar()
    integ.mostrar()


if __name__ == "__main__":
    sistema_polinomios()
