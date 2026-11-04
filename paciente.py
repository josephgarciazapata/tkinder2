"""Paciente de la Entrega 1 (movido de main.py a su propio modulo)."""

from typing import Any


class Paciente:
    """Un paciente. Se compara y ordena por numero de documento.

    Los operadores aceptan tambien un int (el documento), lo que permite
    usar busqueda_binaria y ListaDoble.buscar con solo el numero.
    """

    def __init__(self, documento: int, triage: int, hora_llegada: int) -> None:
        self.documento = documento
        self.triage = triage  # 1 (mas grave) a 5
        self.hora_llegada = hora_llegada  # minuto del dia, 0 a 1440

    def __repr__(self) -> str:
        return (
            f"[Doc:{self.documento} | Triage:{self.triage} | Hora:{self.hora_llegada}]"
        )

    @staticmethod
    def _doc(otro: Any) -> int:
        return otro if isinstance(otro, int) else otro.documento

    def __lt__(self, otro: Any) -> bool:
        return self.documento < self._doc(otro)

    def __le__(self, otro: Any) -> bool:
        return self.documento <= self._doc(otro)

    def __gt__(self, otro: Any) -> bool:
        return self.documento > self._doc(otro)

    def __ge__(self, otro: Any) -> bool:
        return self.documento >= self._doc(otro)

    def __eq__(self, otro: object) -> bool:
        if isinstance(otro, (int, Paciente)):
            return self.documento == self._doc(otro)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.documento)
