"""Colas propias: estatica (circular), dinamica (nodos) y de prioridad (monticulo)."""

import ctypes
from typing import Any

from arreglo_dinamico import ArregloDinamico


class ColaEstatica:
    """Cola FIFO sobre un arreglo circular de tamano fijo.

    Usamos arreglo circular para que encolar y desencolar sean O(1):
    con un arreglo normal habria que correr todos los elementos al sacar
    el primero (el problema de list.pop(0)).
    """

    def __init__(self, capacidad: int) -> None:
        """Crea la cola con el tamano fijo indicado.

        Complejidad: O(capacidad) tiempo, O(capacidad) espacio.
        """
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que 0")
        self.capacidad = capacidad
        self.A = (capacidad * ctypes.py_object)()
        self.inicio = 0  # posicion del primero
        self.n = 0

    def __len__(self) -> int:
        """Cantidad de elementos en la cola.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n

    def esta_vacia(self) -> bool:
        """Dice si la cola no tiene elementos.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n == 0

    def esta_llena(self) -> bool:
        """Dice si la cola uso toda su capacidad.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n == self.capacidad

    def encolar(self, elemento: Any) -> None:
        """Pone un elemento al final. OverflowError si esta llena.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.esta_llena():
            raise OverflowError("La cola esta llena")
        self.A[(self.inicio + self.n) % self.capacidad] = elemento
        self.n += 1

    def desencolar(self) -> Any:
        """Saca y devuelve el primero. IndexError si esta vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.esta_vacia():
            raise IndexError("La cola esta vacia")
        elemento = self.A[self.inicio]
        self.A[self.inicio] = None  # soltamos la referencia
        self.inicio = (self.inicio + 1) % self.capacidad
        self.n -= 1
        return elemento

    def ver_frente(self) -> Any:
        """Devuelve el primero sin sacarlo. IndexError si esta vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.esta_vacia():
            raise IndexError("La cola esta vacia")
        return self.A[self.inicio]


class _NodoCola:
    """Nodo de la cola dinamica: guarda un dato y el nodo que sigue."""

    def __init__(self, dato: Any) -> None:
        self.dato = dato
        self.siguiente: _NodoCola | None = None


class ColaDinamica:
    """Cola FIFO con nodos enlazados y punteros al primero y al ultimo."""

    def __init__(self) -> None:
        """Crea la cola vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        self.primero: _NodoCola | None = None
        self.ultimo: _NodoCola | None = None
        self.n = 0

    def __len__(self) -> int:
        """Cantidad de elementos en la cola.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n

    def esta_vacia(self) -> bool:
        """Dice si la cola no tiene elementos.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return self.n == 0

    def esta_llena(self) -> bool:
        """Una cola dinamica nunca se llena (mismo contrato que la estatica).

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return False

    def encolar(self, elemento: Any) -> None:
        """Pone un elemento al final.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        nuevo = _NodoCola(elemento)
        if self.ultimo is None:
            self.primero = nuevo
        else:
            self.ultimo.siguiente = nuevo
        self.ultimo = nuevo
        self.n += 1

    def desencolar(self) -> Any:
        """Saca y devuelve el primero. IndexError si esta vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.primero is None:
            raise IndexError("La cola esta vacia")
        elemento = self.primero.dato
        self.primero = self.primero.siguiente
        if self.primero is None:
            self.ultimo = None
        self.n -= 1
        return elemento

    def ver_frente(self) -> Any:
        """Devuelve el primero sin sacarlo. IndexError si esta vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.primero is None:
            raise IndexError("La cola esta vacia")
        return self.primero.dato


class ColaPrioridad:
    """Cola de prioridad con monticulo binario de minimos.

    Sale primero la clave MAS PEQUENA. Si dos claves son iguales sale
    primero la que llego antes (se usa un contador de insercion), por
    eso sirve para el triage: clave = (nivel, hora de llegada).
    El monticulo vive en un ArregloDinamico propio, no en heapq.
    """

    def __init__(self) -> None:
        """Crea la cola vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        self._heap = ArregloDinamico()
        self._contador = 0

    def __len__(self) -> int:
        """Cantidad de elementos en la cola.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return len(self._heap)

    def esta_vacia(self) -> bool:
        """Dice si la cola no tiene elementos.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
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
        """Mete un dato con su clave y lo sube hasta su lugar.

        Complejidad: O(log n) tiempo, O(1) espacio.
        """
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
        """Saca y devuelve el dato de menor clave. IndexError si esta vacia.

        Complejidad: O(log n) tiempo, O(1) espacio.
        """
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
        """Devuelve el dato de menor clave sin sacarlo. IndexError si esta vacia.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        if self.esta_vacia():
            raise IndexError("La cola de prioridad esta vacia")
        return self._heap[0][2]
