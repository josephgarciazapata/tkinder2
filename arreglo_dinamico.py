"""Arreglo dinamico propio (Entrega 1, refactorizado en la Entrega 2).

Cambios respecto a la Entrega 1: se agregaron anotaciones de tipo,
docstrings con complejidad, capacidad inicial opcional, __iter__ y
quitar_ultimo (lo necesita el monticulo de la cola de prioridad).
El nombre de los atributos (n, capacidad, A) y la politica de
crecimiento (duplicar) no cambiaron.
"""

import ctypes
from collections.abc import Iterator
from typing import Any


class ArregloDinamico:
    """Arreglo que duplica su capacidad cuando se llena."""

    def __init__(self, capacidad_inicial: int = 1) -> None:
        """Crea el arreglo vacio.

        Complejidad: O(capacidad_inicial) tiempo, O(capacidad_inicial) espacio.
        """
        self.n = 0
        self.capacidad = max(1, capacidad_inicial)
        self.A = self._crear_arreglo(self.capacidad)

    def __len__(self) -> int:
        """Cantidad de elementos.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n

    def __getitem__(self, k: int) -> Any:
        """Devuelve el elemento en la posicion k. IndexError si esta fuera de rango.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if not 0 <= k < self.n:
            raise IndexError("Índice fuera de rango")
        return self.A[k]

    def __setitem__(self, k: int, valor: Any) -> None:
        """Cambia el elemento en la posicion k. IndexError si esta fuera de rango.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if not 0 <= k < self.n:
            raise IndexError("Índice fuera de rango")
        self.A[k] = valor

    def _crear_arreglo(self, capacidad: int) -> Any:
        return (capacidad * ctypes.py_object)()

    def agregar(self, elemento: Any) -> None:
        """Agrega al final; duplica la capacidad si esta lleno.

        Complejidad: O(1) amortizado tiempo (O(n) en la duplicacion),
        O(1) espacio amortizado.
        """
        if self.n == self.capacidad:
            self._redimensionar(2 * self.capacidad)
        self.A[self.n] = elemento
        self.n += 1

    def quitar_ultimo(self) -> Any:
        """Saca y devuelve el ultimo elemento. IndexError si esta vacio.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.n == 0:
            raise IndexError("El arreglo esta vacio")
        self.n -= 1
        elemento = self.A[self.n]
        self.A[self.n] = None  # soltamos la referencia
        return elemento

    def _redimensionar(self, nueva_capacidad: int) -> None:
        B = self._crear_arreglo(nueva_capacidad)
        for k in range(self.n):
            B[k] = self.A[k]
        self.A = B
        self.capacidad = nueva_capacidad

    def __iter__(self) -> Iterator[Any]:
        """Recorre los elementos en orden.

        Complejidad: O(n) tiempo, O(1) espacio.
        """
        for k in range(self.n):
            yield self.A[k]
