import pytest

from arreglo_dinamico import ArregloDinamico
from busqueda import busqueda_binaria
from main import generar_datos
from ordenamiento import merge_sort
from paciente import Paciente

def test_arreglo_vacio() -> None:
    a = ArregloDinamico()
    assert len(a) == 0 and list(a) == []
    with pytest.raises(IndexError):
        a[0]
    with pytest.raises(IndexError):
        a.quitar_ultimo()

def test_arreglo_crece_duplicando() -> None:
    a = ArregloDinamico()
    capacidades = set()
    for i in range(100):
        a.agregar(i)
        capacidades.add(a.capacidad)
    assert capacidades == {1, 2, 4, 8, 16, 32, 64, 128}
    assert list(a) == list(range(100))

def test_arreglo_indices_invalidos_y_asignacion() -> None:
    a = ArregloDinamico()
    a.agregar("x")
    a[0] = "y"
    assert a[0] == "y"
    for k in (-1, 1):
        with pytest.raises(IndexError):
            a[k]
        with pytest.raises(IndexError):
            a[k] = 1

def test_arreglo_quitar_ultimo_n_veces() -> None:
    a = ArregloDinamico()
    for i in range(1000):
        a.agregar(i)
    for i in range(999, -1, -1):
        assert a.quitar_ultimo() == i
    assert len(a) == 0

def test_busqueda_binaria_casos() -> None:
    assert busqueda_binaria([], 1) == -1
    assert busqueda_binaria([5], 5) == 0
    assert busqueda_binaria([5], 4) == -1
    datos = list(range(0, 2000, 2))
    assert busqueda_binaria(datos, 0) == 0
    assert busqueda_binaria(datos, 1998) == 999
    assert busqueda_binaria(datos, 7) == -1

def test_busqueda_binaria_sobre_pacientes_ordenados() -> None:
    censo, documentos = generar_datos(2000, semilla=2)
    merge_sort(censo)
    for doc in documentos[:200]:
        pos = busqueda_binaria(censo, doc)
        assert pos != -1 and censo[pos].documento == doc
    assert busqueda_binaria(censo, 1) == -1

def test_paciente_se_compara_por_documento_o_entero() -> None:
    a, b = Paciente(10, 1, 0), Paciente(20, 5, 9)
    assert a < b and b > a and a <= b and b >= a
    assert a == 10 and a == Paciente(10, 3, 3) and a != b
    assert a != "texto"

def test_generar_datos_unicos_y_en_rango() -> None:
    censo, documentos = generar_datos(3000, semilla=3)
    assert len(censo) == 3000 and len(set(documentos)) == 3000
    assert all(1 <= p.triage <= 5 and 0 <= p.hora_llegada <= 1440 for p in censo)

def test_generar_datos_con_semilla_es_reproducible() -> None:
    a, _ = generar_datos(50, semilla=9)
    b, _ = generar_datos(50, semilla=9)
    assert [p.documento for p in a] == [p.documento for p in b]
