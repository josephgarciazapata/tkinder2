from collections.abc import Iterator
from typing import Any


class NodoDoble:

    def __init__(self, dato: Any) -> None:
        self.dato = dato
        self.anterior: NodoDoble | None = None
        self.siguiente: NodoDoble | None = None


class ListaDoble:


    def __init__(self) -> None:

        self.primero: NodoDoble | None = None
        self.ultimo: NodoDoble | None = None
        self.n: int = 0

    def __len__(self) -> int:

        return self.n

    def esta_vacia(self) -> bool:

        return self.n == 0

    def agregar_al_final(self, dato: Any) -> NodoDoble:

        nuevo = NodoDoble(dato)
        if self.ultimo is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            nuevo.anterior = self.ultimo
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
        self.n += 1
        return nuevo

    def agregar_al_inicio(self, dato: Any) -> NodoDoble:

        nuevo = NodoDoble(dato)
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            nuevo.siguiente = self.primero
            self.primero.anterior = nuevo
            self.primero = nuevo
        self.n += 1
        return nuevo

    def buscar(self, valor: Any) -> Any | None:

        actual = self.primero
        while actual is not None:
            if actual.dato == valor:
                return actual.dato
            actual = actual.siguiente
        return None

    def eliminar(self, valor: Any) -> Any | None:

        actual = self.primero
        while actual is not None:
            if actual.dato == valor:
                self._desconectar(actual)
                return actual.dato
            actual = actual.siguiente
        return None

    def eliminar_nodo(self, nodo: NodoDoble) -> Any:

        dato = nodo.dato
        self._desconectar(nodo)
        return dato

    def _desconectar(self, nodo: NodoDoble) -> None:

        if nodo.anterior is None:
            self.primero = nodo.siguiente
        else:
            nodo.anterior.siguiente = nodo.siguiente

        if nodo.siguiente is None:
            self.ultimo = nodo.anterior
        else:
            nodo.siguiente.anterior = nodo.anterior

        nodo.anterior = None
        nodo.siguiente = None
        self.n -= 1

    def __iter__(self) -> Iterator[Any]:

        actual = self.primero
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def recorrer_al_reves(self) -> Iterator[Any]:

        actual = self.ultimo
        while actual is not None:
            yield actual.dato
            actual = actual.anterior
