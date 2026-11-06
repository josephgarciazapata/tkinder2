import heapq
import os
import random
import time
from collections import deque
from collections.abc import Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from arreglo_dinamico import ArregloDinamico
from cola import ColaDinamica, ColaEstatica, ColaPrioridad
from lista_doble import ListaDoble
from ordenamiento import ordenar_iterativo, ordenar_recursivo
from pila import PilaDinamica, PilaEstatica

TAMANOS = [1000, 2000, 4000, 8000, 16000, 32000]
CARPETA = os.path.dirname(os.path.abspath(__file__))


def medir(funcion: Callable[[int], None], n: int) -> float:
    """Mide cuanto tarda funcion(n), en segundos."""
    inicio = time.perf_counter()
    funcion(n)
    return time.perf_counter() - inicio


def correr(funcion: Callable[[int], None]) -> list[float]:
    """Corre funcion para cada tamano; repite 3 veces y deja el mejor tiempo."""
    return [min(medir(funcion, n) for _ in range(3)) for n in TAMANOS]


# ---- Lista: agregar n elementos al INICIO ----
def lista_doble_inicio(n: int) -> None:
    lista = ListaDoble()
    for i in range(n):
        lista.agregar_al_inicio(i)


def list_python_inicio(n: int) -> None:
    lista: list[int] = []
    for i in range(n):
        lista.insert(0, i)


def deque_inicio(n: int) -> None:
    d: deque[int] = deque()
    for i in range(n):
        d.appendleft(i)


# ---- Lista: borrar n elementos desde posiciones al azar del medio ----
def lista_doble_borrar_medio(n: int) -> None:
    lista = ListaDoble()
    nodos = [lista.agregar_al_final(i) for i in range(n)]
    random.Random(1).shuffle(nodos)
    for nodo in nodos:
        lista.eliminar_nodo(nodo)


def list_python_borrar_medio(n: int) -> None:
    lista = list(range(n))
    azar = random.Random(1)
    while lista:
        lista.pop(azar.randrange(len(lista)))


# ---- Pila: apilar n elementos y desapilarlos todos ----
def pila_dinamica(n: int) -> None:
    pila = PilaDinamica()
    for i in range(n):
        pila.apilar(i)
    while not pila.esta_vacia():
        pila.desapilar()


def pila_estatica(n: int) -> None:
    pila = PilaEstatica(n)
    for i in range(n):
        pila.apilar(i)
    while not pila.esta_vacia():
        pila.desapilar()


def pila_list_python(n: int) -> None:
    pila: list[int] = []
    for i in range(n):
        pila.append(i)  # noqa: PERF402  (el ciclo es lo que se mide)
    while len(pila) > 0:
        pila.pop()


def pila_deque(n: int) -> None:
    pila: deque[int] = deque()
    for i in range(n):
        pila.append(i)
    while len(pila) > 0:
        pila.pop()


# ---- Cola: encolar n elementos y desencolarlos todos ----
def cola_dinamica(n: int) -> None:
    cola = ColaDinamica()
    for i in range(n):
        cola.encolar(i)
    while not cola.esta_vacia():
        cola.desencolar()


def cola_estatica(n: int) -> None:
    cola = ColaEstatica(n)
    for i in range(n):
        cola.encolar(i)
    while not cola.esta_vacia():
        cola.desencolar()


def cola_deque(n: int) -> None:
    cola: deque[int] = deque()
    for i in range(n):
        cola.append(i)
    while len(cola) > 0:
        cola.popleft()


def cola_list_pop0(n: int) -> None:
    cola: list[int] = []
    for i in range(n):
        cola.append(i) 
    while len(cola) > 0:
        cola.pop(0)


def prioridad_propia(n: int) -> None:
    azar = random.Random(2)
    cola = ColaPrioridad()
    for i in range(n):
        cola.insertar(azar.randint(1, 5), i)
    while not cola.esta_vacia():
        cola.extraer_min()


def prioridad_heapq(n: int) -> None:
    azar = random.Random(2)
    h: list[tuple[int, int]] = []
    for i in range(n):
        heapq.heappush(h, (azar.randint(1, 5), i))
    while h:
        heapq.heappop(h)


# ---- Ordenacion: n numeros al azar ----
def _datos(n: int) -> list[float]:
    azar = random.Random(3)
    return [azar.random() for _ in range(n)]


def orden_recursivo(n: int) -> None:
    a = ArregloDinamico()
    for x in _datos(n):
        a.agregar(x)
    ordenar_recursivo(a)


def orden_iterativo(n: int) -> None:
    a = ArregloDinamico()
    for x in _datos(n):
        a.agregar(x)
    ordenar_iterativo(a)


def orden_sorted(n: int) -> None:
    sorted(_datos(n))


def graficar(
    resultados: dict[str, list[float]],
    claves: list[str],
    titulo: str,
    xlabel: str,
    archivo: str,
) -> None:
    plt.figure()
    for k in claves:
        plt.plot(TAMANOS, resultados[k], marker="o", label=k)
    plt.xlabel(xlabel)
    plt.ylabel("Tiempo (s)")
    plt.title(titulo)
    plt.legend()
    plt.savefig(os.path.join(CARPETA, archivo), dpi=120)
    plt.close()


if __name__ == "__main__":
    pruebas: dict[str, Callable[[int], None]] = {
        "ListaDoble.agregar_al_inicio": lista_doble_inicio,
        "list.insert(0, x)": list_python_inicio,
        "deque.appendleft": deque_inicio,
        "ListaDoble.eliminar_nodo (medio)": lista_doble_borrar_medio,
        "list.pop(i) (medio)": list_python_borrar_medio,
        "PilaDinamica": pila_dinamica,
        "PilaEstatica": pila_estatica,
        "list append/pop": pila_list_python,
        "deque append/pop": pila_deque,
        "ColaDinamica": cola_dinamica,
        "ColaEstatica": cola_estatica,
        "deque append/popleft": cola_deque,
        "list append/pop(0)": cola_list_pop0,
        "ColaPrioridad": prioridad_propia,
        "heapq": prioridad_heapq,
        "mezcla recursiva": orden_recursivo,
        "mezcla iterativa": orden_iterativo,
        "sorted()": orden_sorted,
    }
    resultados = {}
    for nombre, f in pruebas.items():
        print("midiendo", nombre, "...", flush=True)
        resultados[nombre] = correr(f)

    print("\n" + "n".ljust(34) + "".join(str(n).rjust(10) for n in TAMANOS))
    for k, tiempos in resultados.items():
        print(k.ljust(34) + "".join(f"{t:10.5f}" for t in tiempos))

    graficar(
        resultados,
        ["ListaDoble.agregar_al_inicio", "list.insert(0, x)", "deque.appendleft"],
        "Agregar al inicio: lista doble vs list vs deque",
        "n (elementos agregados al inicio)",
        "grafica_lista.png",
    )
    graficar(
        resultados,
        ["ListaDoble.eliminar_nodo (medio)", "list.pop(i) (medio)"],
        "Borrar del medio: lista doble (por nodo) vs list",
        "n (elementos borrados al azar)",
        "grafica_lista_borrado.png",
    )
    graficar(
        resultados,
        ["PilaDinamica", "PilaEstatica", "list append/pop", "deque append/pop"],
        "Pilas propias vs list y deque",
        "n (apilar y desapilar n elementos)",
        "grafica_pilas.png",
    )
    graficar(
        resultados,
        ["ColaDinamica", "ColaEstatica", "deque append/popleft", "list append/pop(0)"],
        "Colas propias vs deque y list.pop(0)",
        "n (encolar y desencolar n elementos)",
        "grafica_colas.png",
    )
    graficar(
        resultados,
        ["ColaPrioridad", "heapq"],
        "Cola de prioridad propia vs heapq",
        "n (insertar y extraer n elementos)",
        "grafica_prioridad.png",
    )
    graficar(
        resultados,
        ["mezcla recursiva", "mezcla iterativa", "sorted()"],
        "Ordenacion: mezcla propia vs sorted()",
        "n (elementos a ordenar)",
        "grafica_orden.png",
    )
    print("\nGraficas guardadas en", CARPETA)
