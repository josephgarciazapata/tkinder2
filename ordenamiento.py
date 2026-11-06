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

    _ordenar_rec(arreglo, _relleno(len(arreglo)), 0, len(arreglo), _identidad)

def ordenar_recursivo(
    arreglo: ArregloDinamico, clave: Callable[[Any], Any] = _identidad
) -> ArregloDinamico:

    copia = _copiar(arreglo)
    _ordenar_rec(copia, _relleno(len(copia)), 0, len(copia), clave)
    return copia


def ordenar_iterativo(
    arreglo: ArregloDinamico, clave: Callable[[Any], Any] = _identidad
) -> ArregloDinamico:

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
