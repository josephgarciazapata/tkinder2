"""Busqueda binaria (Entrega 1, con tipos y docstring)."""

from typing import Any


def busqueda_binaria(arreglo: Any, objetivo: Any) -> int:
    """Devuelve la posicion de objetivo en un arreglo ORDENADO, o -1 si no esta.

    Complejidad: O(log n) tiempo, O(1) espacio.
    """
    izquierda = 0
    derecha = len(arreglo) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2

        if arreglo[medio] == objetivo:
            return medio
        elif arreglo[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return -1
