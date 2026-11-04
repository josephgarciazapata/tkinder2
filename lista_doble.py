from collections.abc import Iterator
from typing import Any


class NodoDoble:
    """Un nodo de la lista: guarda un dato y apunta al anterior y al siguiente."""

    def __init__(self, dato: Any) -> None:
        self.dato = dato
        self.anterior: NodoDoble | None = None
        self.siguiente: NodoDoble | None = None


class ListaDoble:
    """Lista doblemente ligada.

    La usamos para guardar los pacientes de cada servicio de urgencias.
    Elegimos lista doble (y no arreglo) porque cuando un paciente sale
    de un servicio (traslado o deshacer una admision) hay que borrarlo
    del medio sin correr todos los demas.
    """

    def __init__(self) -> None:
        """Crea la lista vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        self.primero: NodoDoble | None = None
        self.ultimo: NodoDoble | None = None
        self.n: int = 0

    def __len__(self) -> int:
        """Cantidad de elementos de la lista.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n

    def esta_vacia(self) -> bool:
        """Dice si la lista no tiene elementos.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n == 0

    def agregar_al_final(self, dato: Any) -> NodoDoble:
        """Agrega un dato al final y devuelve su nodo.

        Quien guarde el nodo puede borrarlo despues en O(1) con
        eliminar_nodo, sin buscarlo.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
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
        """Agrega un dato al inicio y devuelve su nodo.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
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
        """Devuelve el dato que sea igual a valor, o None si no esta.

        Para los pacientes, valor puede ser el numero de documento
        (la clase Paciente compara por documento).

        Complejidad: O(n) tiempo, O(1) espacio.
        """
        actual = self.primero
        while actual is not None:
            if actual.dato == valor:
                return actual.dato
            actual = actual.siguiente
        return None

    def eliminar(self, valor: Any) -> Any | None:
        """Borra el primer dato igual a valor y lo devuelve (None si no esta).

        Encontrarlo cuesta O(n), pero una vez encontrado el borrado es
        O(1) porque no hay que mover nada.

        Complejidad: O(n) tiempo, O(1) espacio.
        """
        actual = self.primero
        while actual is not None:
            if actual.dato == valor:
                self._desconectar(actual)
                return actual.dato
            actual = actual.siguiente
        return None

    def eliminar_nodo(self, nodo: NodoDoble) -> Any:
        """Borra un nodo que ya se tiene en la mano y devuelve su dato.

        Es lo que justifica la lista doble: no hay que buscar ni mover
        nada. El nodo debe pertenecer a esta lista.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        dato = nodo.dato
        self._desconectar(nodo)
        return dato

    def _desconectar(self, nodo: NodoDoble) -> None:
        # Casos: el nodo es el primero, el ultimo, o esta en el medio.
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
        """Recorre la lista del primero al ultimo.

        Complejidad: O(n) tiempo, O(1) espacio.
        """
        actual = self.primero
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def recorrer_al_reves(self) -> Iterator[Any]:
        """Recorre la lista del ultimo al primero.

        Complejidad: O(n) tiempo, O(1) espacio.
        """
        actual = self.ultimo
        while actual is not None:
            yield actual.dato
            actual = actual.anterior
