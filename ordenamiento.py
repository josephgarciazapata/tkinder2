"""Ordenacion por mezcla (merge sort).

- merge_sort: la de la Entrega 1 (en el lugar, recursiva). Refactorizada:
  ya no usa list de Python para las mitades, usa ArregloDinamico.
- ordenar_recursivo / ordenar_iterativo: devuelven una copia ordenada y
  aceptan una clave (por ejemplo, triage y hora de llegada).

Por que recursion aqui: ordenar es "ordenar la mitad izquierda, ordenar
la mitad derecha y mezclar", que es la definicion recursiva. La
profundidad de la pila es log2(n): 13 llamadas para 5.000 pacientes,
nunca cerca del limite de Python (1000).

Donde NO se usa recursion: recorrer la ListaDoble nodo a nodo
tendria profundidad n y lanzaria RecursionError con mas de ~1000
pacientes; ahi la version iterativa es la correcta.
"""

from collections.abc import Callable
from typing import Any

from arreglo_dinamico import ArregloDinamico


def _identidad(x: Any) -> Any:
    return x


def _relleno(n: int) -> ArregloDinamico:
    aux = ArregloDinamico(max(1, n))
    for _ in range(n):
        aux.agregar(None)
    return aux


def _copiar(origen: ArregloDinamico) -> ArregloDinamico:
    copia = ArregloDinamico(max(1, len(origen)))
    for x in origen:
        copia.agregar(x)
    return copia


def _mezclar(
    a: ArregloDinamico,
    aux: ArregloDinamico,
    lo: int,
    mid: int,
    hi: int,
    clave: Callable[[Any], Any],
) -> None:
    """Mezcla a[lo:mid] y a[mid:hi], que ya estan ordenados."""
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if clave(a[i]) <= clave(a[j]):  # <= mantiene la estabilidad
            aux[k] = a[i]
            i += 1
        else:
            aux[k] = a[j]
            j += 1
        k += 1
    while i < mid:
        aux[k] = a[i]
        i += 1
        k += 1
    while j < hi:
        aux[k] = a[j]
        j += 1
        k += 1
    for t in range(lo, hi):
        a[t] = aux[t]


def _ordenar_rec(
    a: ArregloDinamico,
    aux: ArregloDinamico,
    lo: int,
    hi: int,
    clave: Callable[[Any], Any],
) -> None:
    if hi - lo <= 1:  # caso base: 0 o 1 elementos ya estan ordenados
        return
    mid = (lo + hi) // 2
    _ordenar_rec(a, aux, lo, mid, clave)
    _ordenar_rec(a, aux, mid, hi, clave)
    _mezclar(a, aux, lo, mid, hi, clave)


def merge_sort(arreglo: ArregloDinamico) -> None:
    """Ordena el arreglo EN EL LUGAR (estable), por el orden natural de sus elementos.

    Es la funcion de la Entrega 1; los pacientes quedan ordenados por documento.

    Complejidad: O(n log n) tiempo, O(n) espacio (arreglo auxiliar) mas
    O(log n) de pila de llamadas.
    """
    _ordenar_rec(arreglo, _relleno(len(arreglo)), 0, len(arreglo), _identidad)


def ordenar_recursivo(
    arreglo: ArregloDinamico, clave: Callable[[Any], Any] = _identidad
) -> ArregloDinamico:
    """Devuelve una copia ordenada (estable) por mezcla recursiva.

    No modifica el arreglo original.

    Complejidad: O(n log n) tiempo, O(n) espacio (copia y auxiliar) mas
    O(log n) de pila de llamadas.
    """
    copia = _copiar(arreglo)
    _ordenar_rec(copia, _relleno(len(copia)), 0, len(copia), clave)
    return copia


def ordenar_iterativo(
    arreglo: ArregloDinamico, clave: Callable[[Any], Any] = _identidad
) -> ArregloDinamico:
    """Devuelve una copia ordenada (estable) por mezcla iterativa (de abajo hacia arriba).

    Es la alternativa sin recursion: mezcla bloques de tamano 1, 2, 4...

    Complejidad: O(n log n) tiempo, O(n) espacio, sin pila de llamadas.
    """
    copia = _copiar(arreglo)
    n = len(copia)
    aux = _relleno(n)
    ancho = 1
    while ancho < n:
        for lo in range(0, n, 2 * ancho):
            mid = min(lo + ancho, n)
            hi = min(lo + 2 * ancho, n)
            _mezclar(copia, aux, lo, mid, hi, clave)
        ancho *= 2
    return copia
