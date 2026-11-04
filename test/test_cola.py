# Autor de las pruebas: ____________  (debe ser distinto del autor de cola.py)
import heapq
import random

import pytest

from cola import ColaDinamica, ColaEstatica, ColaPrioridad


def crear(tipo: str) -> ColaDinamica | ColaEstatica:
    return ColaDinamica() if tipo == "dinamica" else ColaEstatica(10)


@pytest.mark.parametrize("tipo", ["dinamica", "estatica"])
def test_vacia(tipo: str) -> None:
    cola = crear(tipo)
    assert cola.esta_vacia() and len(cola) == 0
    with pytest.raises(IndexError):
        cola.desencolar()
    with pytest.raises(IndexError):
        cola.ver_frente()


@pytest.mark.parametrize("tipo", ["dinamica", "estatica"])
def test_un_elemento_y_orden_fifo(tipo: str) -> None:
    cola = crear(tipo)
    cola.encolar("a")
    assert cola.ver_frente() == "a" and len(cola) == 1
    cola.encolar("b")
    cola.encolar("c")
    assert [cola.desencolar() for _ in range(3)] == ["a", "b", "c"]
    assert cola.esta_vacia()


def test_estatica_llena_da_overflow() -> None:
    cola = ColaEstatica(2)
    cola.encolar(1)
    cola.encolar(2)
    assert cola.esta_llena()
    with pytest.raises(OverflowError):
        cola.encolar(3)
    assert len(cola) == 2 and cola.ver_frente() == 1


def test_estatica_capacidad_invalida() -> None:
    with pytest.raises(ValueError):
        ColaEstatica(0)


def test_estatica_circular_da_muchas_vueltas() -> None:
    cola = ColaEstatica(3)
    siguiente = 0
    esperado = 0
    for _ in range(100):  # da muchas vueltas al arreglo
        while not cola.esta_llena():
            cola.encolar(siguiente)
            siguiente += 1
        for _ in range(2):
            assert cola.desencolar() == esperado
            esperado += 1
    assert len(cola) == 1


def test_dinamica_nunca_se_llena_y_se_reusa() -> None:
    cola = ColaDinamica()
    assert not cola.esta_llena()
    for i in range(3):
        cola.encolar(i)
    for _ in range(3):
        cola.desencolar()
    assert cola.primero is None and cola.ultimo is None
    cola.encolar(9)
    assert cola.ver_frente() == 9


@pytest.mark.parametrize("tipo", ["dinamica", "estatica"])
def test_n_veces(tipo: str) -> None:
    n = 10_000
    cola = ColaDinamica() if tipo == "dinamica" else ColaEstatica(n)
    for i in range(n):
        cola.encolar(i)
    for i in range(n):
        assert cola.desencolar() == i
    assert cola.esta_vacia()


# ---------------- cola de prioridad ----------------


def test_prioridad_vacia() -> None:
    cola = ColaPrioridad()
    assert cola.esta_vacia() and len(cola) == 0
    with pytest.raises(IndexError):
        cola.extraer_min()
    with pytest.raises(IndexError):
        cola.ver_min()


def test_prioridad_un_elemento() -> None:
    cola = ColaPrioridad()
    cola.insertar(5, "x")
    assert cola.ver_min() == "x" and len(cola) == 1
    assert cola.extraer_min() == "x" and cola.esta_vacia()


def test_prioridad_sale_el_menor_primero() -> None:
    cola = ColaPrioridad()
    for clave, dato in [(3, "c"), (1, "a"), (2, "b"), (5, "e"), (4, "d")]:
        cola.insertar(clave, dato)
    assert [cola.extraer_min() for _ in range(5)] == ["a", "b", "c", "d", "e"]


def test_prioridad_empate_sale_el_que_llego_antes() -> None:
    cola = ColaPrioridad()
    for i in range(20):
        cola.insertar(1, i)
    assert [cola.extraer_min() for _ in range(20)] == list(range(20))


def test_prioridad_clave_compuesta_triage_y_llegada() -> None:
    cola = ColaPrioridad()
    cola.insertar((2, 0), "nivel2-temprano")
    cola.insertar((1, 9), "nivel1-tarde")
    cola.insertar((1, 3), "nivel1-temprano")
    assert cola.extraer_min() == "nivel1-temprano"
    assert cola.extraer_min() == "nivel1-tarde"
    assert cola.extraer_min() == "nivel2-temprano"


def test_prioridad_coincide_con_heapq_en_5000_aleatorios() -> None:
    azar = random.Random(3)
    cola = ColaPrioridad()
    referencia: list[tuple[int, int]] = []
    for i in range(5000):
        clave = azar.randint(1, 5)
        cola.insertar(clave, i)
        heapq.heappush(referencia, (clave, i))  # i desempata por llegada
    for _ in range(5000):
        assert cola.extraer_min() == heapq.heappop(referencia)[1]
    assert cola.esta_vacia()


def test_prioridad_mezclando_insertar_y_extraer() -> None:
    azar = random.Random(4)
    cola = ColaPrioridad()
    referencia: list[tuple[int, int]] = []
    for i in range(3000):
        if referencia and azar.random() < 0.4:
            assert cola.extraer_min() == heapq.heappop(referencia)[1]
        else:
            clave = azar.randint(1, 5)
            cola.insertar(clave, i)
            heapq.heappush(referencia, (clave, i))
    assert len(cola) == len(referencia)
