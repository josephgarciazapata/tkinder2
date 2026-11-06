from typing import Any

from arreglo_dinamico import ArregloDinamico
from cola import ColaDinamica, ColaEstatica, ColaPrioridad
from lista_doble import ListaDoble, NodoDoble
from ordenamiento import ordenar_recursivo
from pila import PilaDinamica, PilaEstatica


class Servicio:

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.pacientes = ListaDoble()


class Consultorio:

    def __init__(self, numero: int, cola: ColaDinamica | ColaEstatica) -> None:
        self.numero = numero
        self.cola = cola


class SistemaUrgencias:

    def __init__(
        self,
        nombres_servicios: list[str],
        tipo_pila: str = "dinamica",
        capacidad_pila: int = 1000,
        n_consultorios: int = 3,
        tipo_cola: str = "dinamica",
        capacidad_cola: int = 1000,
    ) -> None:

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

        return (paciente.triage, paciente.hora_llegada)

    def _poner(self, paciente: Any, servicio: Servicio) -> None:
        nodo = servicio.pacientes.agregar_al_final(paciente)
        self._indice[paciente.documento] = (servicio, nodo)

    def _sacar(self, documento: int) -> Any:
        servicio, nodo = self._indice.pop(documento)
        return servicio.pacientes.eliminar_nodo(nodo)


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

        self.reversos.apilar(("admision", paciente, nombre_servicio))
        self._poner(paciente, servicio)

    def trasladar(self, documento: int, origen: str, destino: str) -> None:

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

        if self.reversos.esta_vacia():
            return None
        registro = self.reversos.desapilar()
        tipo = registro[0]
        paciente = registro[1]

        if tipo == "admision":
            self._sacar(paciente.documento)
            return "Se deshizo la admision del paciente " + str(paciente.documento)


        s_origen = self._buscar_servicio(registro[2])
        self._sacar(paciente.documento)
        self._poner(paciente, s_origen)
        return "Se deshizo el traslado del paciente " + str(paciente.documento)

    def cantidad_en(self, nombre_servicio: str) -> int:

        return len(self._buscar_servicio(nombre_servicio).pacientes)

    def pacientes_ordenados(self, nombre_servicio: str) -> ArregloDinamico:

        servicio = self._buscar_servicio(nombre_servicio)
        arreglo = ArregloDinamico()
        for paciente in servicio.pacientes:
            arreglo.agregar(paciente)
        return ordenar_recursivo(arreglo, self._clave)



    def registrar_llegada(self, paciente: Any) -> None:

        self.espera.insertar(self._clave(paciente), paciente)

    def esperando(self) -> int:

        return len(self.espera)

    def llamar_a_consultorio(self, numero: int) -> Any | None:

        consultorio = self._buscar_consultorio(numero)
        if self.espera.esta_vacia():
            return None
        if consultorio.cola.esta_llena():
            raise OverflowError("La cola del consultorio esta llena")
        paciente = self.espera.extraer_min()
        consultorio.cola.encolar(paciente)
        return paciente

    def atender(self, numero: int) -> Any | None:

        consultorio = self._buscar_consultorio(numero)
        if consultorio.cola.esta_vacia():
            return None
        return consultorio.cola.desencolar()
