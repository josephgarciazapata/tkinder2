import ctypes
from collections.abc import Iterator
from typing import Any


class ArregloDinamico:


    def __init__(self, capacidad_inicial: int = 1) -> None:

        self.n = 0
        self.capacidad = max(1, capacidad_inicial)
        self.A = self._crear_arreglo(self.capacidad)

    def __len__(self) -> int:

        return self.n

    def __getitem__(self, k: int) -> Any:

        if not 0 <= k < self.n:
            raise IndexError("Índice fuera de rango")
        return self.A[k]

    def __setitem__(self, k: int, valor: Any) -> None:

        if not 0 <= k < self.n:
            raise IndexError("Índice fuera de rango")
        self.A[k] = valor

    def _crear_arreglo(self, capacidad: int) -> Any:
        return (capacidad * ctypes.py_object)()

    def agregar(self, elemento: Any) -> None:

        if self.n == self.capacidad:
            self._redimensionar(2 * self.capacidad)
        self.A[self.n] = elemento
        self.n += 1

    def quitar_ultimo(self) -> Any:

        if self.n == 0:
            raise IndexError("El arreglo esta vacio")
        self.n -= 1
        elemento = self.A[self.n]
        self.A[self.n] = None 
        return elemento

    def _redimensionar(self, nueva_capacidad: int) -> None:
        B = self._crear_arreglo(nueva_capacidad)
        for k in range(self.n):
            B[k] = self.A[k]
        self.A = B
        self.capacidad = nueva_capacidad

    def __iter__(self) -> Iterator[Any]:

        for k in range(self.n):
            yield self.A[k]
