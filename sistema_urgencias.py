from typing import Any

from arreglo_dinamico import ArregloDinamico
from cola import ColaDinamica, ColaEstatica, ColaPrioridad
from lista_doble import ListaDoble, NodoDoble
from ordenamiento import ordenar_recursivo
from pila import PilaDinamica, PilaEstatica


class Servicio:
    """Un servicio del hospital (urgencias generales, observacion, etc.).

    Los pacientes del servicio viven en una lista doblemente ligada.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.pacientes = ListaDoble()


class Consultorio:
    """Un consultorio con su cola FIFO de pacientes asignados."""

    def __init__(self, numero: int, cola: ColaDinamica | ColaEstatica) -> None:
        self.numero = numero
        self.cola = cola


class SistemaUrgencias:
    """Nucleo dinamico del sistema: listas, pilas y colas trabajando juntas.

    - Cada servicio guarda sus pacientes en una ListaDoble. Un indice
      documento -> (servicio, nodo) permite sacar a un paciente del
      medio de la lista en O(1) (traslado o deshacer), que es la razon
      de haber elegido lista doble y no arreglo.
    - Cada admision o traslado se anota en una pila de reversos para
      poder deshacer una admision mal registrada.
    - Los pacientes que llegan esperan en una cola de prioridad: sale
      primero el de menor nivel de triage y, a igual nivel, el que
      llego antes. Desde ahi pasan a la cola FIFO de un consultorio.

    La pila y las colas de consultorio pueden ser dinamicas o estaticas
    (tipo_pila, tipo_cola) para compararlas en el informe.

    Nota para el informe (regla de la caja negra): el dict del indice
    esta fuera del nucleo bajo estudio; solo indexa por documento y no
    reemplaza ninguna estructura del curso.
    """

    def __init__(
        self,
        nombres_servicios: list[str],
        tipo_pila: str = "dinamica",
        capacidad_pila: int = 1000,
        n_consultorios: int = 3,
        tipo_cola: str = "dinamica",
        capacidad_cola: int = 1000,
    ) -> None:
        """Crea servicios, pila de reversos, sala de espera y consultorios.

        Complejidad: O(s + c) tiempo, O(s + c) espacio (mas O(capacidad)
        por cada estructura estatica), con s servicios y c consultorios.
        """
        self.servicios = ArregloDinamico()
        for nombre in nombres_servicios:
            self.servicios.agregar(Servicio(nombre))

        self.reversos: PilaEstatica | PilaDinamica
        if tipo_pila == "estatica":
            self.reversos = PilaEstatica(capacidad_pila)
        else:
            self.reversos = PilaDinamica()

        self.espera = ColaPrioridad()
        self.consultorios = ArregloDinamico()
        for numero in range(n_consultorios):
            cola: ColaDinamica | ColaEstatica
            if tipo_cola == "estatica":
                cola = ColaEstatica(capacidad_cola)
            else:
                cola = ColaDinamica()
            self.consultorios.agregar(Consultorio(numero, cola))

        self._indice: dict[int, tuple[Servicio, NodoDoble]] = {}

    # ---------- ayudas internas ----------

    def _buscar_servicio(self, nombre: str) -> Servicio:
        for i in range(len(self.servicios)):
            if self.servicios[i].nombre == nombre:
                return self.servicios[i]
        raise ValueError("No existe el servicio: " + str(nombre))

    def _buscar_consultorio(self, numero: int) -> Consultorio:
        if not 0 <= numero < len(self.consultorios):
            raise ValueError("No existe el consultorio: " + str(numero))
        return self.consultorios[numero]

    @staticmethod
    def _clave(paciente: Any) -> tuple[int, int]:
        # Menor triage primero; a igual triage, el que llego antes.
        # Hora de llegada: el campo hora_llegada de Paciente.
        return (paciente.triage, paciente.hora_llegada)

    def _poner(self, paciente: Any, servicio: Servicio) -> None:
        nodo = servicio.pacientes.agregar_al_final(paciente)
        self._indice[paciente.documento] = (servicio, nodo)

    def _sacar(self, documento: int) -> Any:
        servicio, nodo = self._indice.pop(documento)
        return servicio.pacientes.eliminar_nodo(nodo)

    # ---------- servicios: lista doble + pila de reversos ----------

    def donde_esta(self, documento: int) -> str | None:
        """Devuelve el nombre del servicio donde esta el paciente, o None.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        entrada = self._indice.get(documento)
        return None if entrada is None else entrada[0].nombre

    def admitir(self, paciente: Any, nombre_servicio: str) -> None:
        """Mete un paciente nuevo en un servicio.

        Da ValueError si el servicio no existe o el paciente ya esta
        admitido. Da OverflowError si la pila estatica esta llena.

        Complejidad: O(s) tiempo (buscar el servicio), O(1) espacio.
        """
        servicio = self._buscar_servicio(nombre_servicio)
        if paciente.documento in self._indice:
            raise ValueError("El paciente ya esta admitido")
        # Primero apilamos: si la pila estatica esta llena falla aqui y
        # el paciente no queda a medias.
        self.reversos.apilar(("admision", paciente, nombre_servicio))
        self._poner(paciente, servicio)

    def trasladar(self, documento: int, origen: str, destino: str) -> None:
        """Pasa un paciente de un servicio a otro.

        Da ValueError si algun servicio no existe o el paciente no esta
        en el servicio de origen.

        Complejidad: O(s) tiempo, O(1) espacio (el borrado es O(1)).
        """
        s_origen = self._buscar_servicio(origen)
        s_destino = self._buscar_servicio(destino)
        entrada = self._indice.get(documento)
        if entrada is None or entrada[0] is not s_origen:
            raise ValueError("El paciente no esta en el servicio de origen")
        paciente = entrada[1].dato
        self.reversos.apilar(("traslado", paciente, origen, destino))
        self._sacar(documento)
        self._poner(paciente, s_destino)

    def deshacer(self) -> str | None:
        """Deshace la ultima admision o traslado.

        Devuelve el texto de lo que deshizo, o None si no habia nada.
        Si se deshace un traslado, el paciente vuelve al final de la
        lista del servicio de origen (no recuerda su posicion exacta).

        Complejidad: O(s) tiempo, O(1) espacio.
        """
        if self.reversos.esta_vacia():
            return None
        registro = self.reversos.desapilar()
        tipo = registro[0]
        paciente = registro[1]

        if tipo == "admision":
            self._sacar(paciente.documento)
            return "Se deshizo la admision del paciente " + str(paciente.documento)

        # si no fue admision, fue traslado
        s_origen = self._buscar_servicio(registro[2])
        self._sacar(paciente.documento)
        self._poner(paciente, s_origen)
        return "Se deshizo el traslado del paciente " + str(paciente.documento)

    def cantidad_en(self, nombre_servicio: str) -> int:
        """Cantidad de pacientes que hay en un servicio.

        Complejidad: O(s) tiempo, O(1) espacio.
        """
        return len(self._buscar_servicio(nombre_servicio).pacientes)

    def pacientes_ordenados(self, nombre_servicio: str) -> ArregloDinamico:
        """Pacientes de un servicio ordenados por triage y luego por llegada.

        Usa la mezcla recursiva (profundidad log p, sin riesgo de
        desbordar la pila con datos reales).

        Complejidad: O(p log p) tiempo, O(p) espacio, con p pacientes
        en el servicio.
        """
        servicio = self._buscar_servicio(nombre_servicio)
        arreglo = ArregloDinamico()
        for paciente in servicio.pacientes:
            arreglo.agregar(paciente)
        return ordenar_recursivo(arreglo, self._clave)

    # ---------- sala de espera y consultorios: colas ----------

    def registrar_llegada(self, paciente: Any) -> None:
        """Pone al paciente en la sala de espera (cola de prioridad).

        Complejidad: O(log n) tiempo, O(1) espacio, con n esperando.
        """
        self.espera.insertar(self._clave(paciente), paciente)

    def esperando(self) -> int:
        """Cantidad de pacientes en la sala de espera.

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        return len(self.espera)

    def llamar_a_consultorio(self, numero: int) -> Any | None:
        """Pasa el paciente mas urgente de la sala de espera al consultorio.

        Devuelve el paciente, o None si no habia nadie esperando. Da
        ValueError si el consultorio no existe y OverflowError si su
        cola estatica esta llena (en ese caso nadie sale de la espera).

        Complejidad: O(log n) tiempo, O(1) espacio.
        """
        consultorio = self._buscar_consultorio(numero)
        if self.espera.esta_vacia():
            return None
        if consultorio.cola.esta_llena():
            raise OverflowError("La cola del consultorio esta llena")
        paciente = self.espera.extraer_min()
        consultorio.cola.encolar(paciente)
        return paciente

    def atender(self, numero: int) -> Any | None:
        """Atiende al primero de la cola del consultorio y lo devuelve (o None).

        Complejidad: O(1) tiempo, O(1) espacio.
        """
        consultorio = self._buscar_consultorio(numero)
        if consultorio.cola.esta_vacia():
            return None
        return consultorio.cola.desencolar()
