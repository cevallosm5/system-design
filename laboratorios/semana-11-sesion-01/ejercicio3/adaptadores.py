"""Los adaptadores de la cancelacion. RelojDelSistema y NotificadorPorCorreo
ya estan completos; los demas son tuyos."""

import sqlite3
import time

import correo_simulado
from dominio import Reserva
from puertos import Notificador, Reloj, RepositorioDeReservas


class RepositorioSqlite(RepositorioDeReservas):
    def __init__(self, ruta_base_de_datos):
        self.conexion = sqlite3.connect(ruta_base_de_datos)
        self.conexion.execute(
            "CREATE TABLE IF NOT EXISTS reservas ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "estudiante TEXT, cancha TEXT, fecha TEXT, hora INTEGER)"
        )
        self.conexion.execute("CREATE TABLE IF NOT EXISTS penalizaciones (estudiante TEXT)")

    def agregar(self, estudiante, cancha, fecha, hora):
        cursor = self.conexion.execute(
            "INSERT INTO reservas (estudiante, cancha, fecha, hora) VALUES (?, ?, ?, ?)",
            (estudiante, cancha, fecha, hora),
        )
        self.conexion.commit()
        return Reserva("r-" + str(cursor.lastrowid), estudiante, cancha, fecha, hora)

    def buscar(self, id_reserva):
        fila = self.conexion.execute(
            "SELECT estudiante, cancha, fecha, hora FROM reservas WHERE id = ?",
            (int(id_reserva[2:]),),
        ).fetchone()
        if fila is None:
            return None
        return Reserva(id_reserva, *fila)

    def borrar(self, id_reserva):
        self.conexion.execute("DELETE FROM reservas WHERE id = ?", (int(id_reserva[2:]),))
        self.conexion.commit()

    def registrar_penalizacion(self, estudiante):
        self.conexion.execute(
            "INSERT INTO penalizaciones (estudiante) VALUES (?)", (estudiante,)
        )
        self.conexion.commit()

    def penalizaciones_de(self, estudiante):
        fila = self.conexion.execute(
            "SELECT COUNT(*) FROM penalizaciones WHERE estudiante = ?", (estudiante,)
        ).fetchone()
        return fila[0]


class RepositorioEnMemoria(RepositorioDeReservas):
    def __init__(self):
        self.reservas = {}
        self.penalizaciones = {}
        self.siguiente_id = 1

    def agregar(self, estudiante, cancha, fecha, hora):
        id_reserva = "r-" + str(self.siguiente_id)
        self.siguiente_id += 1
        reserva = Reserva(id_reserva, estudiante, cancha, fecha, hora)
        self.reservas[id_reserva] = reserva
        return reserva

    def buscar(self, id_reserva):
        return self.reservas.get(id_reserva)

    def borrar(self, id_reserva):
        self.reservas.pop(id_reserva, None)

    def registrar_penalizacion(self, estudiante):
        self.penalizaciones[estudiante] = self.penalizaciones.get(estudiante, 0) + 1

    def penalizaciones_de(self, estudiante):
        return self.penalizaciones.get(estudiante, 0)


class RelojFijo(Reloj):
    def __init__(self, fecha, hora):
        self.fecha = fecha
        self.hora = hora

    def ahora(self):
        return (self.fecha, self.hora)


class RelojDelSistema(Reloj):
    def ahora(self):
        return (time.strftime("%Y-%m-%d"), time.localtime().tm_hour)


class NotificadorEnMemoria(Notificador):
    def __init__(self):
        self.enviados = []

    def notificar(self, estudiante, mensaje):
        self.enviados.append((estudiante, mensaje))


class NotificadorPorCorreo(Notificador):
    def notificar(self, estudiante, mensaje):
        correo_simulado.enviar_correo(estudiante, mensaje)
