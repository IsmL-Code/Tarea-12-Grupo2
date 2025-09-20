# reprecentamos un proceso en un sistema operativo simulado
class Proceso:
    def __init__(self, pid, nombre, estado, tiempo_creacion, tiempo_cpu):
        self.pid = pid  # Identificador único del proceso
        self.nombre = nombre  # Nombre del proceso por ejemplo: Chrome, VSCode
        self.estado = estado  # Estado del proceso: 'listo', 'en ejecucion', 'bloqueado', 'terminado'
        self.tiempo_creacion = tiempo_creacion  # Tiempo de creación del proceso
        self.tiempo_cpu = tiempo_cpu  # Tiempo de CPU requerido
        self.siguiente = None  # Referencia al siguiente proceso para lista enlazada

#  definimos una clase que gestiona una lista enlazada de procesos
class ListaProcesos:
    def __init__(self):
        self.cabeza = None  # Inicio de la lista

    def añadir_proceso(self, pid, nombre, estado, tiempo_creacion, tiempo_cpu):
        # Añadimos un nuevo proceso al final de la lista
        nuevo = Proceso(pid, nombre, estado, tiempo_creacion, tiempo_cpu)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def cambiar_estado(self, pid, nuevo_estado):
        # Cambiamos el estado de un proceso dado su PID
        actual = self.cabeza
        while actual:
            if actual.pid == pid:
                actual.estado = nuevo_estado
                return True
            actual = actual.siguiente
        return False  # No se encontró el proceso

    def eliminar_terminados(self):
        # Eliminamos todos los procesos cuyo estado sea 'terminado'
        while self.cabeza and self.cabeza.estado == "terminado":
            self.cabeza = self.cabeza.siguiente

        actual = self.cabeza
        while actual and actual.siguiente:
            if actual.siguiente.estado == "terminado":
                actual.siguiente = actual.siguiente.siguiente
            else:
                actual = actual.siguiente

    def mover_al_principio(self, pid):
        # Muevemos un proceso al principio de la lista (simula asignarle prioridad)
        if not self.cabeza or self.cabeza.pid == pid:
            return  #  analizamos  la lista vacía o el proceso ya está al principio

        prev = None
        actual = self.cabeza
        while actual and actual.pid != pid:
            prev = actual
            actual = actual.siguiente

        if actual:
            prev.siguiente = actual.siguiente
            actual.siguiente = self.cabeza
            self.cabeza = actual

    def mostrar_procesos(self):
        # Muestramos la lista de procesos en formato de tabla
        actual = self.cabeza
        print(f"{'PID':<5}{'Nombre':<15}{'Estado':<12}{'Creación':<10}{'CPU Req.':<10}")
        print("-" * 55)
        while actual:
            print(f"{actual.pid:<5}{actual.nombre:<15}{actual.estado:<12}{actual.tiempo_creacion:<10}{actual.tiempo_cpu:<10}")
            actual = actual.siguiente

    def tiempo_promedio_espera(self):
        # Calculamos el tiempo promedio de espera de los procesos no terminados
        suma_espera = 0
        contador = 0
        actual = self.cabeza
        while actual:
            if actual.estado != "terminado":
                suma_espera += actual.tiempo_creacion
                contador += 1
            actual = actual.siguiente
        return (suma_espera / contador) if contador > 0 else 0

# mostramos cómo funciona el sistema de procesos
def sistema_gestion():
    lista = ListaProcesos()

    # Lista de procesos iniciales (PID, Nombre, Estado, Tiempo Creación, Tiempo CPU)    
    procesos = [
        (1, "Chrome", "listo", 0, 20),
        (2, "Spotify", "bloqueado", 2, 15),
        (3, "VSCode", "en ejecucion", 1, 25),
        (4, "Terminal", "listo", 3, 10),
        (5, "Slack", "terminado", 4, 8),
        (6, "Docker", "listo", 5, 30),
        (7, "Firefox", "en ejecucion", 6, 22),
        (8, "Mail", "bloqueado", 7, 5),
        (9, "Zoom", "listo", 8, 12),
        (10, "Notepad", "listo", 9, 3)
    ]

    # Añadimos todos los procesos a la lista
    for p in procesos:
        lista.añadir_proceso(*p)

    # Mostramos la lista inicial de procesos
    print("Procesos iniciales:")
    lista.mostrar_procesos()

    # Cambiamos el estado de un proceso
    print("\nCambiar estado PID 2 a listo")
    lista.cambiar_estado(2, "listo")
    lista.mostrar_procesos()

    # Movemos un proceso al principio de la lista (simula prioridad)
    print("\nMover PID 7 al principio (simula prioridad)")
    lista.mover_al_principio(7)
    lista.mostrar_procesos()

    # Eliminamos los procesos terminados
    print("\nEliminar procesos terminados")
    lista.eliminar_terminados()
    lista.mostrar_procesos()

    # Calculamos y mostramos los tiempo promedio de espera
    print("\nTiempo promedio de espera:", lista.tiempo_promedio_espera())


if __name__ == "__main__":
    sistema_gestion()
