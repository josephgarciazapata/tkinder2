from typing import Any
class Paciente:

    def __init__(self, documento: int, triage: int, hora_llegada: int) -> None:
        self.documento = documento
        self.triage = triage  
        self.hora_llegada = hora_llegada  

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
