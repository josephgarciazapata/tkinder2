# Autor de las pruebas: ____________  (debe ser distinto del autor de sistema_urgencias.py)
import pytest

from main import generar_datos
from paciente import Paciente
from sistema_urgencias import SistemaUrgencias

SERVICIOS = ["Urgencias", "Observacion", "Cirugia"]


def p(doc: int, triage: int = 3, llegada: int = 0) -> Paciente:
    return Paciente(doc, triage, llegada)


def nuevo(**kw) -> SistemaUrgencias:
    return SistemaUrgencias(SERVICIOS, **kw)


# ---------- servicios, lista doble y pila ----------


def test_admitir_y_donde_esta() -> None:
    s = nuevo()
    s.admitir(p(1), "Urgencias")
    assert s.donde_esta(1) == "Urgencias"
    assert s.donde_esta(999) is None
    assert s.cantidad_en("Urgencias") == 1


def test_admitir_repetido_o_servicio_inexistente() -> None:
    s = nuevo()
    s.admitir(p(1), "Urgencias")
    with pytest.raises(ValueError):
        s.admitir(p(1), "Cirugia")
    with pytest.raises(ValueError):
        s.admitir(p(2), "Marte")
    assert s.cantidad_en("Cirugia") == 0


def test_trasladar_y_deshacer() -> None:
    s = nuevo()
    s.admitir(p(1), "Observacion")
    s.trasladar(1, "Observacion", "Cirugia")
    assert s.donde_esta(1) == "Cirugia"
    assert "traslado" in s.deshacer()
    assert s.donde_esta(1) == "Observacion"
    assert s.cantidad_en("Cirugia") == 0


def test_trasladar_desde_servicio_equivocado() -> None:
    s = nuevo()
    s.admitir(p(1), "Observacion")
    with pytest.raises(ValueError):
        s.trasladar(1, "Cirugia", "Urgencias")
    with pytest.raises(ValueError):
        s.trasladar(77, "Observacion", "Cirugia")
    assert s.donde_esta(1) == "Observacion"


def test_deshacer_admision_y_pila_vacia() -> None:
    s = nuevo()
    assert s.deshacer() is None
    s.admitir(p(1), "Urgencias")
    assert "admision" in s.deshacer()
    assert s.donde_esta(1) is None and s.cantidad_en("Urgencias") == 0
    assert s.deshacer() is None


def test_deshacer_varias_veces_en_orden_inverso() -> None:
    s = nuevo()
    s.admitir(p(1), "Urgencias")
    s.admitir(p(2), "Urgencias")
    s.trasladar(1, "Urgencias", "Cirugia")
    s.deshacer()  # traslado
    s.deshacer()  # admision de 2
    assert s.donde_esta(1) == "Urgencias" and s.donde_esta(2) is None


def test_pila_estatica_llena_no_deja_admision_a_medias() -> None:
    s = nuevo(tipo_pila="estatica", capacidad_pila=2)
    s.admitir(p(1), "Urgencias")
    s.admitir(p(2), "Urgencias")
    with pytest.raises(OverflowError):
        s.admitir(p(3), "Urgencias")
    assert s.donde_esta(3) is None and s.cantidad_en("Urgencias") == 2


@pytest.mark.parametrize("tipo", ["dinamica", "estatica"])
def test_5000_admisiones_y_deshacerlas_todas(tipo: str) -> None:
    censo, _ = generar_datos(5000)
    s = nuevo(tipo_pila=tipo, capacidad_pila=5000)
    for i in range(len(censo)):
        s.admitir(censo[i], "Urgencias")
    assert s.cantidad_en("Urgencias") == 5000
    for _ in range(5000):
        s.deshacer()
    assert s.cantidad_en("Urgencias") == 0 and s.deshacer() is None


def test_pacientes_ordenados_por_triage_y_llegada() -> None:
    s = nuevo()
    for doc, triage, llegada in [(1, 3, 5), (2, 1, 9), (3, 3, 2), (4, 1, 1)]:
        s.admitir(p(doc, triage, llegada), "Urgencias")
    orden = [x.documento for x in s.pacientes_ordenados("Urgencias")]
    assert orden == [4, 2, 3, 1]


# ---------- sala de espera y consultorios ----------


def test_sala_de_espera_vacia() -> None:
    s = nuevo()
    assert s.esperando() == 0
    assert s.llamar_a_consultorio(0) is None
    assert s.atender(0) is None


def test_llama_primero_al_mas_urgente_y_desempata_por_llegada() -> None:
    s = nuevo()
    s.registrar_llegada(p(1, triage=3, llegada=0))
    s.registrar_llegada(p(2, triage=1, llegada=5))
    s.registrar_llegada(p(3, triage=1, llegada=2))
    llamados = [s.llamar_a_consultorio(0).documento for _ in range(3)]
    assert llamados == [3, 2, 1]


def test_consultorio_es_fifo() -> None:
    s = nuevo()
    s.registrar_llegada(p(1, 2, 0))
    s.registrar_llegada(p(2, 1, 1))
    s.llamar_a_consultorio(1)
    s.llamar_a_consultorio(1)
    assert s.atender(1).documento == 2  # entro primero porque era mas urgente
    assert s.atender(1).documento == 1
    assert s.atender(1) is None


def test_consultorio_inexistente() -> None:
    with pytest.raises(ValueError):
        nuevo().llamar_a_consultorio(9)
    with pytest.raises(ValueError):
        nuevo().atender(-1)


def test_cola_estatica_de_consultorio_llena_no_pierde_al_paciente() -> None:
    s = nuevo(tipo_cola="estatica", capacidad_cola=1)
    s.registrar_llegada(p(1))
    s.registrar_llegada(p(2))
    s.llamar_a_consultorio(0)
    with pytest.raises(OverflowError):
        s.llamar_a_consultorio(0)
    assert s.esperando() == 1  # el 2 sigue esperando


def test_nadie_de_nivel_i_espera_mas_que_uno_de_nivel_ii() -> None:
    """Criterio de exito del proyecto, sobre 5.000 pacientes."""
    censo, _ = generar_datos(5000)
    s = nuevo()
    for i in range(len(censo)):
        s.registrar_llegada(censo[i])
    posicion: dict[int, int] = {}
    n = 0
    while s.esperando() > 0:
        llamado = s.llamar_a_consultorio(n % 3)
        posicion[llamado.documento] = n
        n += 1
        s.atender((n - 1) % 3)
    ultimo_nivel1 = max(
        posicion[censo[i].documento] for i in range(len(censo)) if censo[i].triage == 1
    )
    primero_nivel2 = min(
        posicion[censo[i].documento] for i in range(len(censo)) if censo[i].triage == 2
    )
    assert ultimo_nivel1 < primero_nivel2
