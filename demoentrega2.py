import random
import time

from main import generar_datos  
from sistema_urgencias import SistemaUrgencias

SERVICIOS = ["Urgencias", "Observacion", "Cirugia"]

if __name__ == "__main__":
    print("\n1. Generando los pacientes de la Entrega 1")
    censo, documentos = generar_datos(5000)
    print("Pacientes generados:", len(censo))

    print("\n2. Admitiendo los pacientes en los servicios (lista doble + pila)")
    sistema = SistemaUrgencias(SERVICIOS, tipo_pila="dinamica", n_consultorios=3)
    azar = random.Random(7)
    inicio = time.perf_counter()
    for i in range(len(censo)):
        paciente = censo[i]

        if paciente.triage <= 2:
            servicio = "Urgencias"
        else:
            servicio = azar.choice(["Observacion", "Cirugia"])
        sistema.admitir(paciente, servicio)
    fin = time.perf_counter()
    print("Tiempo de admision:", round(fin - inicio, 4), "segundos")
    for nombre in SERVICIOS:
        print(" ", nombre, ":", sistema.cantidad_en(nombre), "pacientes")

    print("\n3. Trasladando un paciente de Observacion a Cirugia")
    paciente = None
    for p in sistema.servicios[1].pacientes:  
        paciente = p
        break
    doc = paciente.documento
    print("Antes:", sistema.donde_esta(doc))
    sistema.trasladar(doc, "Observacion", "Cirugia")
    print("Despues:", sistema.donde_esta(doc))

    print("\n4. Deshaciendo el traslado")
    print(sistema.deshacer())
    print("Ahora esta en:", sistema.donde_esta(doc))

    print("\n5. Deshaciendo la ultima admision mal registrada")
    total = lambda: sum(sistema.cantidad_en(n) for n in SERVICIOS)
    antes = total()
    print(sistema.deshacer())
    print("Pacientes antes:", antes, "- despues:", total())

    print("\n6. Sala de espera: cola de prioridad + cola FIFO por consultorio")
    inicio = time.perf_counter()
    for i in range(len(censo)):
        sistema.registrar_llegada(censo[i])
    print(
        "Esperando:",
        sistema.esperando(),
        "pacientes,",
        round(time.perf_counter() - inicio, 4),
        "s",
    )
    llamados = []
    while sistema.esperando() > 0:
        for c in range(3):
            p = sistema.llamar_a_consultorio(c)
            if p is not None:
                llamados.append(p)
    triages = [p.triage for p in llamados]
    ordenado = all(triages[i] <= triages[i + 1] for i in range(len(triages) - 1))
    print("Primeros 10 llamados (triage):", triages[:10])
    print("Ningun nivel menos urgente fue llamado antes que uno mas urgente:", ordenado)
    primero = sistema.atender(0)
    print("Consultorio 0 atiende primero a:", primero)

    print("\n7. Pacientes de Cirugia ordenados por triage y llegada (mezcla recursiva)")
    ordenados = sistema.pacientes_ordenados("Cirugia")
    print("Primeros 3:", [ordenados[i] for i in range(3)])
