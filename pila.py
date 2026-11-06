import ctypes
from typing import Any


class PilaEstatica:

    def __init__(self, capacidad: int) -> None:

        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que 0")
        self.capacidad = capacidad
        self.A = (capacidad * ctypes.py_object)()
        self.n = 0

    def __len__(self) -> int:

        return self.n

    def esta_vacia(self) -> bool:

        return self.n == 0

    def esta_llena(self) -> bool:

        return self.n == self.capacidad

    def apilar(self, elemento: Any) -> None:

        if self.esta_llena():
            raise OverflowError("La pila esta llena")
        self.A[self.n] = elemento
        self.n += 1

    def desapilar(self) -> Any:

        if self.esta_vacia():
            raise IndexError("La pila esta vacia")
        self.n -= 1
        elemento = self.A[self.n]
        self.A[self.n] = None  
        return elemento

    def tope(self) -> Any:

        if self.esta_vacia():
            raise IndexError("La pila esta vacia")
        return self.A[self.n - 1]


class _NodoPila:


    def __init__(self, dato: Any, abajo: "_NodoPila | None") -> None:
        self.dato = dato
        self.abajo = abajo  


class PilaDinamica:

    def __init__(self) -> None:

        self.cima: _NodoPila | None = None
        self.n = 0

    def __len__(self) -> int:

        return self.n

    def esta_vacia(self) -> bool:

        return self.n == 0

    def apilar(self, elemento: Any) -> None:

        self.cima = _NodoPila(elemento, self.cima)
        self.n += 1

    def desapilar(self) -> Any:

        if self.cima is None:
            raise IndexError("La pila esta vacia")
        elemento = self.cima.dato
        self.cima = self.cima.abajo
        self.n -= 1
        return elemento

    def tope(self) -> Any:

        if self.cima is None:
            raise IndexError("La pila esta vacia")
        return self.cima.dato
