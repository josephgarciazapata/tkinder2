# Autor de las pruebas: ____________  (debe ser distinto del autor de lista_doble.py)
import pytest

from lista_doble import ListaDoble


def lista_de(*valores: int) -> ListaDoble:
    lista = ListaDoble()
    for v in valores:
        lista.agregar_al_final(v)
    return lista


def test_vacia() -> None:
    lista = ListaDoble()
    assert len(lista) == 0 and lista.esta_vacia()
    assert list(lista) == [] and list(lista.recorrer_al_reves()) == []
    assert lista.buscar(1) is None
    assert lista.eliminar(1) is None


def test_un_elemento() -> None:
    lista = lista_de(7)
    assert len(lista) == 1
    assert lista.primero is lista.ultimo
    assert lista.eliminar(7) == 7
    assert lista.primero is None and lista.ultimo is None and len(lista) == 0


def test_agregar_inicio_y_final_en_ambos_sentidos() -> None:
    lista = ListaDoble()
    lista.agregar_al_final(2)
    lista.agregar_al_inicio(1)
    lista.agregar_al_final(3)
    assert list(lista) == [1, 2, 3]
    assert list(lista.recorrer_al_reves()) == [3, 2, 1]


def test_eliminar_extremos_y_medio() -> None:
    lista = lista_de(0, 1, 2, 3, 4)
    assert lista.eliminar(0) == 0  # primero
    assert lista.eliminar(4) == 4  # ultimo
    assert lista.eliminar(2) == 2  # medio
    assert list(lista) == [1, 3]
    assert list(lista.recorrer_al_reves()) == [3, 1]
    assert len(lista) == 2


def test_eliminar_inexistente_no_cambia_nada() -> None:
    lista = lista_de(1, 2, 3)
    assert lista.eliminar(99) is None
    assert list(lista) == [1, 2, 3] and len(lista) == 3


def test_buscar_encuentra_el_cero() -> None:
    assert lista_de(0).buscar(0) == 0


def test_agregar_devuelve_el_nodo_y_eliminar_nodo_es_o1() -> None:
    lista = ListaDoble()
    nodos = [lista.agregar_al_final(i) for i in range(5)]
    assert lista.eliminar_nodo(nodos[2]) == 2
    assert lista.eliminar_nodo(nodos[0]) == 0
    assert lista.eliminar_nodo(nodos[4]) == 4
    assert list(lista) == [1, 3]
    assert list(lista.recorrer_al_reves()) == [3, 1]


def test_operacion_repetida_n_veces() -> None:
    lista = ListaDoble()
    n = 5000
    for i in range(n):
        lista.agregar_al_inicio(i)
    assert len(lista) == n
    assert list(lista) == list(range(n - 1, -1, -1))
    for i in range(n):
        lista.eliminar(i)
    assert len(lista) == 0 and lista.primero is None and lista.ultimo is None


def test_enlaces_consistentes_tras_borrados_aleatorios() -> None:
    import random

    azar = random.Random(1)
    lista = ListaDoble()
    nodos = [lista.agregar_al_final(i) for i in range(500)]
    azar.shuffle(nodos)
    esperado = list(range(500))
    for nodo in nodos[:300]:
        lista.eliminar_nodo(nodo)
        esperado.remove(nodo.dato)
    assert list(lista) == esperado
    assert list(lista.recorrer_al_reves()) == esperado[::-1]


@pytest.mark.parametrize("valor", [None, "x"])
def test_buscar_inexistente(valor: object) -> None:
    assert lista_de(1, 2).buscar(valor) is None
