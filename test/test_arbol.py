import pytest
from paciente import Paciente
from arbol import ArbolPacientes

def test_insertar_y_buscar_arbol():
    arbol = ArbolPacientes()
    arbol.insertar(Paciente(50, 2, 10))
    arbol.insertar(Paciente(30, 1, 15))
    
    assert arbol.buscar(50).documento == 50
    assert arbol.buscar(30).triage == 1
    assert arbol.buscar(99) is None

def test_recorrido_in_order_ordena_ascendente():
    arbol = ArbolPacientes()
    for doc in [50, 30, 70, 20, 40, 60, 80]:
        arbol.insertar(Paciente(doc, 3, 0))
        
    resultado = arbol.in_order()
    docs_ordenados = [p.documento for p in resultado]
    assert docs_ordenados == [20, 30, 40, 50, 60, 70, 80]

def test_eliminar_nodo_hoja_y_un_hijo():
    arbol = ArbolPacientes()
    arbol.insertar(Paciente(50, 3, 0))
    arbol.insertar(Paciente(30, 3, 0))
    arbol.insertar(Paciente(20, 3, 0))
    
    arbol.eliminar(20)
    assert arbol.buscar(20) is None
    
    arbol.eliminar(30)
    assert arbol.buscar(30) is None

def test_eliminar_nodo_dos_hijos():
    arbol = ArbolPacientes()
    for doc in [50, 30, 70, 60, 80]:
        arbol.insertar(Paciente(doc, 3, 0))
        
    arbol.eliminar(70)
    assert arbol.buscar(70) is None
    
    resultado = arbol.in_order()
    docs = [p.documento for p in resultado]
    assert docs == [30, 50, 60, 80]

def test_eliminar_inexistente_lanza_error():
    arbol = ArbolPacientes()
    arbol.insertar(Paciente(10, 1, 1))
    with pytest.raises(ValueError):
        arbol.eliminar(99)