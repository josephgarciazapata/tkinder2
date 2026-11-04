import ctypes
from typing import Any


class PilaEstatica:
    """Pila con un arreglo de tamano fijo.

    El tamano se decide al crearla y no cambia. Si se llena, apilar
    da error.
    """

    def __init__(self, capacidad: int) -> None:
        """Crea la pila con el tamano fijo indicado.

        Complejidad: O(capacidad) tiempo, O(capacidad) espacio.
        """
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que 0")
        self.capacidad = capacidad
        self.A = (capacidad * ctypes.py_object)()
        self.n = 0

    def __len__(self) -> int:
        """Cantidad de elementos apilados.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n

    def esta_vacia(self) -> bool:
        """Dice si la pila no tiene elementos.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n == 0

    def esta_llena(self) -> bool:
        """Dice si la pila ya uso toda su capacidad.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n == self.capacidad

    def apilar(self, elemento: Any) -> None:
        """Pone un elemento en la cima. Da OverflowError si esta llena.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.esta_llena():
            raise OverflowError("La pila esta llena")
        self.A[self.n] = elemento
        self.n += 1

    def desapilar(self) -> Any:
        """Saca y devuelve el elemento de la cima. Da IndexError si esta vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.esta_vacia():
            raise IndexError("La pila esta vacia")
        self.n -= 1
        elemento = self.A[self.n]
        self.A[self.n] = None  # soltamos la referencia
        return elemento

    def tope(self) -> Any:
        """Devuelve la cima sin sacarla. Da IndexError si esta vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.esta_vacia():
            raise IndexError("La pila esta vacia")
        return self.A[self.n - 1]


class _NodoPila:
    """Nodo de la pila dinamica: guarda un dato y el nodo de abajo."""

    def __init__(self, dato: Any, abajo: "_NodoPila | None") -> None:
        self.dato = dato
        self.abajo = abajo  # el nodo que quedo debajo


class PilaDinamica:
    """Pila hecha con nodos enlazados. Crece hasta donde alcance la memoria."""

    def __init__(self) -> None:
        """Crea la pila vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        self.cima: _NodoPila | None = None
        self.n = 0

    def __len__(self) -> int:
        """Cantidad de elementos apilados.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n

    def esta_vacia(self) -> bool:
        """Dice si la pila no tiene elementos.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n == 0

    def apilar(self, elemento: Any) -> None:
        """Pone un elemento en la cima.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        self.cima = _NodoPila(elemento, self.cima)
        self.n += 1

    def desapilar(self) -> Any:
        """Saca y devuelve el elemento de la cima. Da IndexError si esta vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.cima is None:
            raise IndexError("La pila esta vacia")
        elemento = self.cima.dato
        self.cima = self.cima.abajo
        self.n -= 1
        return elemento

    def tope(self) -> Any:
        """Devuelve la cima sin sacarla. Da IndexError si esta vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.cima is None:
            raise IndexError("La pila esta vacia")
        return self.cima.dato
