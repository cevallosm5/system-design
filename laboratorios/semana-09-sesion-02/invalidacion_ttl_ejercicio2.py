"""Ejercicio 2: invalidar el cache al reservar, y darle a cada entrada un
tiempo de vida (TTL).

Corre las pruebas con:

    pytest test_invalidacion_ttl_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""


class ServicioConInvalidacionYTTL:
    def __init__(self, repositorio, reloj, ttl):
        self.repositorio = repositorio
        self.reloj = reloj
        self.ttl = ttl
        self.cache = {}
        self.aciertos = 0
        self.fallos = 0

    def disponibilidad(self, cancha, fecha):
        clave = (cancha, fecha)
        entrada = self.cache.get(clave)
        if entrada is not None:
            libres, instante = entrada
            if self.reloj.ahora() - instante < self.ttl:
                self.aciertos += 1
                return libres

        self.fallos += 1
        libres = self.repositorio.consultar_disponibilidad(cancha, fecha)
        self.cache[clave] = (libres, self.reloj.ahora())
        return libres

    def reservar(self, cancha, fecha, hora):
        libres = self.repositorio.consultar_disponibilidad(cancha, fecha)
        if hora not in libres:
            return False
        self.repositorio.registrar_reserva(cancha, fecha, hora)
        self.cache.pop((cancha, fecha), None)
        return True
