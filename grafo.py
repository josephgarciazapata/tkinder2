from lista_doble import ListaDoble
from cola import ColaDinamica
from arreglo_dinamico import ArregloDinamico

class GrafoHospital:
    def __init__(self) -> None:
        self.adyacencia: dict[str, ListaDoble] = {}

    def agregar_servicio(self, nombre: str) -> None:
        if nombre not in self.adyacencia:
            self.adyacencia[nombre] = ListaDoble()

    def agregar_conexion(self, origen: str, destino: str) -> None:
        if origen not in self.adyacencia or destino not in self.adyacencia:
            raise ValueError("Ambos servicios deben existir en el grafo")
        
        if self.adyacencia[origen].buscar(destino) is None:
            self.adyacencia[origen].agregar_al_final(destino)
            self.adyacencia[destino].agregar_al_final(origen)

    def bfs_recorrido(self, inicio: str) -> ArregloDinamico:
        if inicio not in self.adyacencia:
            raise ValueError("El servicio de inicio no existe")

        visitados = set()
        resultado = ArregloDinamico()
        cola = ColaDinamica()

        cola.encolar(inicio)
        visitados.add(inicio)

        while not cola.esta_vacia():
            actual = cola.desencolar()
            resultado.agregar(actual)

            for vecino in self.adyacencia[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.encolar(vecino)

        return resultado

    def camino_mas_corto(self, origen: str, destino: str) -> ArregloDinamico | None:
        if origen not in self.adyacencia or destino not in self.adyacencia:
            raise ValueError("Ambos servicios deben existir en el grafo")

        visitados = {origen}
        padres: dict[str, str | None] = {origen: None}
        cola = ColaDinamica()
        cola.encolar(origen)

        encontrado = False
        while not cola.esta_vacia():
            actual = cola.desencolar()

            if actual == destino:
                encontrado = True
                break

            for vecino in self.adyacencia[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = actual
                    cola.encolar(vecino)

        if not encontrado:
            return None

        camino = ArregloDinamico()
        nodo_actual = destino
        pila_temp = []
        
        while nodo_actual is not None:
            pila_temp.append(nodo_actual)
            nodo_actual = padres[nodo_actual]

        while pila_temp:
            camino.agregar(pila_temp.pop())

        return camino