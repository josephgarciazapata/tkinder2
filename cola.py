import ctypes
from typing import Any

from arreglo_dinamico import ArregloDinamico


class ColaEstatica:

    def __init__(self, capacidad: int) -> None:

        if capacidad <= 0:
            raise ValueError
        self.capacidad = capacidad
        self.A = (capacidad * ctypes.py_object)()
        self.inicio = 0  # posicion del primero
        self.n = 0

    def __len__(self) -> int:

        return self.n

    def esta_vacia(self) -> bool:

        return self.n == 0

    def esta_llena(self) -> bool:

        return self.n == self.capacidad

    def encolar(self, elemento: Any) -> None:

        if self.esta_llena():
            raise OverflowError("La cola esta llena")
        self.A[(self.inicio + self.n) % self.capacidad] = elemento
        self.n += 1

    def desencolar(self) -> Any:

        if self.esta_vacia():
            raise IndexError("La cola esta vacia")
        elemento = self.A[self.inicio]
        self.A[self.inicio] = None  # soltamos la referencia
        self.inicio = (self.inicio + 1) % self.capacidad
        self.n -= 1
        return elemento

    def ver_frente(self) -> Any:

        if self.esta_vacia():
            raise IndexError("La cola esta vacia")
        return self.A[self.inicio]


class _NodoCola:


    def __init__(self, dato: Any) -> None:
        self.dato = dato
        self.siguiente: _NodoCola | None = None


class ColaDinamica:


    def __init__(self) -> None:

        self.primero: _NodoCola | None = None
        self.ultimo: _NodoCola | None = None
        self.n = 0

    def __len__(self) -> int:

        return self.n

    def esta_vacia(self) -> bool:

        return self.n == 0

    def esta_llena(self) -> bool:

        return False

    def encolar(self, elemento: Any) -> None:

        nuevo = _NodoCola(elemento)
        if self.ultimo is None:
            self.primero = nuevo
        else:
            self.ultimo.siguiente = nuevo
        self.ultimo = nuevo
        self.n += 1

    def desencolar(self) -> Any:

        if self.primero is None:
            raise IndexError("La cola esta vacia")
        elemento = self.primero.dato
        self.primero = self.primero.siguiente
        if self.primero is None:
            self.ultimo = None
        self.n -= 1
        return elemento

    def ver_frente(self) -> Any:

        if self.primero is None:
            raise IndexError("La cola esta vacia")
        return self.primero.dato


class ColaPrioridad:

    def __init__(self) -> None:

        self._heap = ArregloDinamico()
        self._contador = 0

    def __len__(self) -> int:

        return len(self._heap)

    def esta_vacia(self) -> bool:

        return len(self._heap) == 0

    def _menor(self, i: int, j: int) -> bool:
        a = self._heap[i]
        b = self._heap[j]
        return (a[0], a[1]) < (b[0], b[1])

    def _intercambiar(self, i: int, j: int) -> None:
        temp = self._heap[i]
        self._heap[i] = self._heap[j]
        self._heap[j] = temp

    def insertar(self, clave: Any, dato: Any) -> None:

        self._heap.agregar((clave, self._contador, dato))
        self._contador += 1
        i = len(self._heap) - 1
        while i > 0:
            padre = (i - 1) // 2
            if not self._menor(i, padre):
                break
            self._intercambiar(i, padre)
            i = padre

    def extraer_min(self) -> Any:

        if self.esta_vacia():
            raise IndexError("La cola de prioridad esta vacia")
        n = len(self._heap)
        self._intercambiar(0, n - 1)
        _, _, dato = self._heap.quitar_ultimo()
        n -= 1
        i = 0
        while True:
            izq = 2 * i + 1
            der = izq + 1
            menor = i
            if izq < n and self._menor(izq, menor):
                menor = izq
            if der < n and self._menor(der, menor):
                menor = der
            if menor == i:
                break
            self._intercambiar(i, menor)
            i = menor
        return dato

    def ver_min(self) -> Any:

        if self.esta_vacia():
            raise IndexError("La cola de prioridad esta vacia")
        return self._heap[0][2]
