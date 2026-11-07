"""Los casos de uso de ReservaU: lo que la aplicacion hace, paso a paso.
Solo conoce el dominio y los puertos.
"""

from dominio import motivo_de_rechazo, texto_de_hora


class ReservarCancha:
    def __init__(self, repositorio, notificador):
        self.repositorio = repositorio
        self.notificador = notificador

    def ejecutar(self, estudiante, cancha, fecha, hora):
        hora_ocupada = self.repositorio.ocupada(cancha, fecha, hora)
        reservas_del_dia = self.repositorio.contar_del_estudiante(estudiante, fecha)
        motivo = motivo_de_rechazo(cancha, hora, hora_ocupada, reservas_del_dia)
        if motivo is not None:
            return {"estado": "rechazada", "motivo": motivo}
        reserva = self.repositorio.guardar(estudiante, cancha, fecha, hora)
        self.notificador.notificar(
            estudiante,
            f"Reserva {reserva.id} confirmada: {cancha}, {fecha} a las {texto_de_hora(hora)}",
        )
        return {"estado": "confirmada", "reserva": reserva}
