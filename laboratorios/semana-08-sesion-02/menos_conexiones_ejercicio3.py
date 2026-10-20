"""Ejercicio 3: balanceador de menos conexiones (least connections).

Corre las pruebas con:

    pytest test_menos_conexiones_ejercicio3.py

Las pruebas tambien usan tu BalanceadorRoundRobin del Ejercicio 2, para
comparar los dos algoritmos con el mismo trafico.
"""


class BalanceadorMenosConexiones:
    def __init__(self, servidores):
        self.servidores = servidores

    def enviar(self, duracion):
        # TODO: elige, entre los servidores sanos que todavia pueden
        # atender, el que tiene menos conexiones activas en este momento.
        # Si hay empate, gana el que aparece primero en la lista.
        # Enviale la solicitud y devuelve su nombre. Si ningun servidor
        # puede atenderla, devuelve None.

        elegido = None
        minimo = float("inf")

        for servidor in self.servidores:
            if servidor.health_check() and servidor.puede_atender():
                conexiones = servidor.conexiones_activas()
                if conexiones < minimo:
                    elegido = servidor
                    minimo = conexiones
        if elegido is not None and elegido.atender(duracion):
            return elegido.nombre
    
        return None
