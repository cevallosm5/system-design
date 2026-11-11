"""Ejercicio 2: el agregado CalendarioDeCancha.

Un CalendarioDeCancha es el calendario de una cancha en un dia, con todas
sus reservas adentro. Es la raiz del agregado: nadie de afuera crea,
mueve ni borra una Reserva directamente; todo pasa por sus metodos, y
cada metodo deja el calendario cumpliendo sus dos reglas:

- Dos reservas del calendario no se solapan.
- Un estudiante no tiene mas de MAXIMO_HORAS_POR_ESTUDIANTE horas
  reservadas en este calendario.

Cuando una operacion romperia una regla, el metodo lanza ValueError con el
motivo y no cambia nada. Usa FranjaHoraria y Reserva de
franja_ejercicio1.py, completo.

Corre las pruebas con:

    pytest test_calendario_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from franja_ejercicio1 import FranjaHoraria, Reserva

MAXIMO_HORAS_POR_ESTUDIANTE = 2


class CalendarioDeCancha:
    def __init__(self, cancha, fecha):
        self.cancha = cancha
        self.fecha = fecha
        self._reservas = {}

    def horas_de(self, estudiante):
        total = 0 

        for reserva in self._reservas.values():
            if reserva.estudiante == estudiante:
                total += reserva.franja.duracion()

        return total

    def choca_con_otra(self, franja, id_a_ignorar=None):
        for id_reserva, reserva in self._reservas.items():
            if id_reserva != id_a_ignorar and reserva.franja.se_solapa_con(franja):
                return True
        return False

    def reservar(self, id_reserva, estudiante, inicio, fin):
        franja = FranjaHoraria(self.fecha, inicio, fin)

        if id_reserva in self._reservas:
            raise ValueError("id repetido")

        if self.choca_con_otra(franja):
            raise ValueError("franja ocupada")

        if self.horas_de(estudiante) + franja.duracion() > MAXIMO_HORAS_POR_ESTUDIANTE:
            raise ValueError("limite de horas alcanzado")

        self._reservas[id_reserva] = Reserva(id_reserva, estudiante, franja)
        

    def mover(self, id_reserva, nuevo_inicio, nuevo_fin):
        if id_reserva not in self._reservas:
            raise ValueError("reserva desconocida")

        reserva = self._reservas[id_reserva]

        nueva_franja = FranjaHoraria(self.fecha, nuevo_inicio, nuevo_fin)

        if self.choca_con_otra(nueva_franja, id_reserva):
            raise ValueError("franja ocupada")

        horas_actuales = self.horas_de(reserva.estudiante) - reserva.franja.duracion()

        if horas_actuales + nueva_franja.duracion() > MAXIMO_HORAS_POR_ESTUDIANTE:
            raise ValueError("limite de horas alcanzado")

        reserva.franja = nueva_franja


    def cancelar(self, id_reserva):
        if id_reserva not in self._reservas:
            raise ValueError("reserva desconocida")
        del self._reservas[id_reserva]

    def reservas(self):
        reservas_ordenadas = sorted(
            self._reservas.values(), key=lambda reserva: reserva.franja.inicio
        )
        return [
            (reserva.id, reserva.estudiante, reserva.franja)
            for reserva in reservas_ordenadas
        ]
