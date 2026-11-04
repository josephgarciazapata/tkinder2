import random
import time
from arreglo_dinamico import ArregloDinamico
from ordenamiento import merge_sort
from busqueda import busqueda_binaria

class Paciente:
    def __init__(self, documento, triage, hora_llegada):
        self.documento = documento
        self.triage = triage
        self.hora_llegada = hora_llegada

    def __repr__(self):
        return f"[Doc:{self.documento} | Triage:{self.triage} | Hora:{self.hora_llegada}]"

    def __lt__(self, otro):
        if isinstance(otro, int):
            return self.documento < otro
        return self.documento < otro.documento

    def __le__(self, otro):
        if isinstance(otro, int):
            return self.documento <= otro
        return self.documento <= otro.documento

    def __gt__(self, otro):
        if isinstance(otro, int):
            return self.documento > otro
        return self.documento > otro.documento

    def __eq__(self, otro):
        if isinstance(otro, int):
            return self.documento == otro
        return self.documento == otro.documento


def generar_datos(cantidad, semilla=None):

    azar = random.Random(semilla) if semilla is not None else random
    
    censo = ArregloDinamico()
    documentos_usados = set()
    
    while len(censo) < cantidad:
        doc = azar.randint(10000000, 99999999)
        if doc not in documentos_usados:
            documentos_usados.add(doc)
            triage = azar.randint(1, 5)
            hora = azar.randint(0, 1440)
            paciente = Paciente(doc, triage, hora)
            censo.agregar(paciente)
            
    return censo, list(documentos_usados)


if __name__ == "__main__":
    
    print("\n1. Generando censo de pacientes ")
    censo_pacientes, documentos = generar_datos(5000)
    print(f"Pacientes generados en el Arreglo Dinámico: {len(censo_pacientes)}")

    print("\n2. Ordenando con Merge Sort ")
    inicio = time.time()
    merge_sort(censo_pacientes)
    fin = time.time()
    print(f"Tiempo de ordenamiento: {fin - inicio:.4f} segundos")

    doc_a_buscar = random.choice(documentos)
    print(f"\n3. Búsqueda Binaria para el documento: {doc_a_buscar}")
    posicion = busqueda_binaria(censo_pacientes, doc_a_buscar)

    if posicion != -1:
        print(f" Paciente encontrado en el índice {posicion}.")
        print(f"Datos: {censo_pacientes[posicion]}")
    else:
        print(" Paciente no encontrado.")