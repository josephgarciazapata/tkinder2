from paciente import Paciente
from arreglo_dinamico import ArregloDinamico

class NodoArbol:
    def __init__(self, paciente: Paciente) -> None:
        self.paciente = paciente
        self.izquierdo: 'NodoArbol | None' = None
        self.derecho: 'NodoArbol | None' = None

class ArbolPacientes:
    def __init__(self) -> None:
        self.raiz: NodoArbol | None = None

    def insertar(self, paciente: Paciente) -> None:
        if self.raiz is None:
            self.raiz = NodoArbol(paciente)
        else:
            self._insertar_rec(self.raiz, paciente)

    def _insertar_rec(self, nodo: NodoArbol, paciente: Paciente) -> None:
        if paciente.documento < nodo.paciente.documento:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(paciente)
            else:
                self._insertar_rec(nodo.izquierdo, paciente)
        elif paciente.documento > nodo.paciente.documento:
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(paciente)
            else:
                self._insertar_rec(nodo.derecho, paciente)
        else:
            raise ValueError("El paciente ya existe en el árbol")

    def buscar(self, documento: int) -> Paciente | None:
        return self._buscar_rec(self.raiz, documento)

    def _buscar_rec(self, nodo: NodoArbol | None, documento: int) -> Paciente | None:
        if nodo is None:
            return None
        if documento == nodo.paciente.documento:
            return nodo.paciente
        elif documento < nodo.paciente.documento:
            return self._buscar_rec(nodo.izquierdo, documento)
        else:
            return self._buscar_rec(nodo.derecho, documento)

    def in_order(self) -> ArregloDinamico:
        resultado = ArregloDinamico()
        self._in_order_rec(self.raiz, resultado)
        return resultado

    def _in_order_rec(self, nodo: NodoArbol | None, resultado: ArregloDinamico) -> None:
        if nodo is not None:
            self._in_order_rec(nodo.izquierdo, resultado)
            resultado.agregar(nodo.paciente)
            self._in_order_rec(nodo.derecho, resultado)

    def pre_order(self) -> ArregloDinamico:
        resultado = ArregloDinamico()
        self._pre_order_rec(self.raiz, resultado)
        return resultado

    def _pre_order_rec(self, nodo: NodoArbol | None, resultado: ArregloDinamico) -> None:
        if nodo is not None:
            resultado.agregar(nodo.paciente)
            self._pre_order_rec(nodo.izquierdo, resultado)
            self._pre_order_rec(nodo.derecho, resultado)

    def eliminar(self, documento: int) -> None:
        self.raiz, eliminado = self._eliminar_rec(self.raiz, documento)
        if not eliminado:
            raise ValueError("Paciente no encontrado")

    def _eliminar_rec(self, nodo: NodoArbol | None, documento: int) -> tuple[NodoArbol | None, bool]:
        if nodo is None:
            return None, False

        eliminado = False
        if documento < nodo.paciente.documento:
            nodo.izquierdo, eliminado = self._eliminar_rec(nodo.izquierdo, documento)
        elif documento > nodo.paciente.documento:
            nodo.derecho, eliminado = self._eliminar_rec(nodo.derecho, documento)
        else:
            eliminado = True
            if nodo.izquierdo is None:
                return nodo.derecho, eliminado
            elif nodo.derecho is None:
                return nodo.izquierdo, eliminado

            sucesor = self._minimo(nodo.derecho)
            nodo.paciente = sucesor.paciente
            nodo.derecho, _ = self._eliminar_rec(nodo.derecho, sucesor.paciente.documento)

        return nodo, eliminado

    def _minimo(self, nodo: NodoArbol) -> NodoArbol:
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual