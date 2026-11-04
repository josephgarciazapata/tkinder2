# Autor de las pruebas: ____________  (debe ser distinto del autor de ordenar.py)
import random
import sys

import pytest

from arreglo_dinamico import ArregloDinamico
from ordenamiento import ordenar_iterativo, ordenar_recursivo


def arreglo_de(valores: list[int]) -> ArregloDinamico:
    a = ArregloDinamico()
    for v in valores:
        a.agregar(v)
    return a


@pytest.mark.parametrize("ordenar", [ordenar_recursivo, ordenar_iterativo])
@pytest.mark.parametrize(
    "valores", [[], [1], [2, 1], [1, 2], [3, 3, 3], [5, 4, 3, 2, 1]]
)
def test_casos_borde(ordenar, valores: list[int]) -> None:
    assert list(ordenar(arreglo_de(valores))) == sorted(valores)


@pytest.mark.parametrize("ordenar", [ordenar_recursivo, ordenar_iterativo])
def test_igual_que_sorted_en_mil_aleatorios(ordenar) -> None:
    azar = random.Random(5)
    valores = [azar.randint(-1000, 1000) for _ in range(1000)]
    assert list(ordenar(arreglo_de(valores))) == sorted(valores)


@pytest.mark.parametrize("ordenar", [ordenar_recursivo, ordenar_iterativo])
def test_no_modifica_el_original(ordenar) -> None:
    original = arreglo_de([3, 1, 2])
    ordenar(original)
    assert list(original) == [3, 1, 2]


@pytest.mark.parametrize("ordenar", [ordenar_recursivo, ordenar_iterativo])
def test_es_estable(ordenar) -> None:
    azar = random.Random(6)
    pares = [(azar.randint(1, 5), i) for i in range(500)]
    resultado = list(ordenar(arreglo_de(pares), lambda p: p[0]))  # type: ignore[arg-type]
    assert resultado == sorted(pares, key=lambda p: p[0])  # sorted tambien es estable


def test_recursivo_no_desborda_la_pila_con_datos_reales() -> None:
    n = 50_000  # log2(50000) ~ 16 niveles, muy lejos de sys.getrecursionlimit()
    azar = random.Random(7)
    valores = [azar.random() for _ in range(n)]
    assert n > sys.getrecursionlimit()
    assert list(ordenar_recursivo(arreglo_de(valores))) == sorted(valores)


# ---------- merge_sort de la Entrega 1 (en el lugar) ----------


def test_merge_sort_en_el_lugar_igual_que_sorted_en_mil() -> None:
    from ordenamiento import merge_sort

    azar = random.Random(8)
    valores = [azar.randint(-1000, 1000) for _ in range(1000)]
    a = arreglo_de(valores)
    merge_sort(a)
    assert list(a) == sorted(valores)


@pytest.mark.parametrize("valores", [[], [1], [2, 1], [1, 1, 1]])
def test_merge_sort_casos_borde(valores: list[int]) -> None:
    from ordenamiento import merge_sort

    a = arreglo_de(valores)
    merge_sort(a)
    assert list(a) == sorted(valores)


def test_merge_sort_ordena_pacientes_por_documento() -> None:
    from main import generar_datos
    from ordenamiento import merge_sort

    censo, _ = generar_datos(1000, semilla=1)
    merge_sort(censo)
    documentos = [p.documento for p in censo]
    assert documentos == sorted(documentos)
