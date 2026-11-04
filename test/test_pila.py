# Autor de las pruebas: ____________  (debe ser distinto del autor de pila.py)
import pytest

from pila import PilaDinamica, PilaEstatica


def crear(tipo: str) -> PilaDinamica | PilaEstatica:
    return PilaDinamica() if tipo == "dinamica" else PilaEstatica(10)


@pytest.mark.parametrize("tipo", ["dinamica", "estatica"])
def test_vacia(tipo: str) -> None:
    pila = crear(tipo)
    assert pila.esta_vacia() and len(pila) == 0
    with pytest.raises(IndexError):
        pila.desapilar()
    with pytest.raises(IndexError):
        pila.tope()


@pytest.mark.parametrize("tipo", ["dinamica", "estatica"])
def test_un_elemento_y_orden_lifo(tipo: str) -> None:
    pila = crear(tipo)
    pila.apilar("a")
    assert pila.tope() == "a" and len(pila) == 1
    pila.apilar("b")
    pila.apilar("c")
    assert [pila.desapilar() for _ in range(3)] == ["c", "b", "a"]
    assert pila.esta_vacia()


@pytest.mark.parametrize("tipo", ["dinamica", "estatica"])
def test_tope_no_saca(tipo: str) -> None:
    pila = crear(tipo)
    pila.apilar(1)
    pila.tope()
    pila.tope()
    assert len(pila) == 1


def test_estatica_llena_da_overflow_y_no_pierde_datos() -> None:
    pila = PilaEstatica(2)
    pila.apilar(1)
    pila.apilar(2)
    assert pila.esta_llena()
    with pytest.raises(OverflowError):
        pila.apilar(3)
    assert len(pila) == 2 and pila.tope() == 2


def test_estatica_capacidad_invalida() -> None:
    with pytest.raises(ValueError):
        PilaEstatica(0)


def test_estatica_se_puede_reusar_despues_de_vaciarse() -> None:
    pila = PilaEstatica(3)
    for ronda in range(5):
        for i in range(3):
            pila.apilar(i + ronda)
        for _ in range(3):
            pila.desapilar()
    assert pila.esta_vacia()


@pytest.mark.parametrize("tipo", ["dinamica", "estatica"])
def test_n_veces(tipo: str) -> None:
    n = 10_000
    pila = PilaDinamica() if tipo == "dinamica" else PilaEstatica(n)
    for i in range(n):
        pila.apilar(i)
    assert len(pila) == n
    for i in range(n - 1, -1, -1):
        assert pila.desapilar() == i
    assert pila.esta_vacia()
