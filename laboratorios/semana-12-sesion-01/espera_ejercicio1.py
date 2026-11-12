"""Ejercicio 1: la lista de espera, primero consultando y despues con
Observer.

Parte A (ya escrita, no la cambies): beto quiere la cancha-1 el martes de
18 a 19, que ana tiene reservada. La app de beto consulta cada cierto
numero de segundos si la franja se libero. ana cancela a los 5500 segundos
(poco mas de hora y media). simular_consultas cuenta cuantas consultas hizo la app
hasta que beto se entero.

Parte B (TODO 1 a 3): el calendario avisa cuando una franja se libera, a
quien se haya suscrito. Nadie pregunta.

Corre el archivo con:

    python3 espera_ejercicio1.py

y las pruebas con:

    pytest test_espera_ejercicio1.py
"""

from notificaciones import NotificadorEnMemoria
from reservas import CalendarioDeCancha, FranjaHoraria

SEGUNDO_DE_LA_CANCELACION = 5500


# ---------------------------------------------------------------- Parte A

def simular_consultas(intervalo_segundos):
    calendario = CalendarioDeCancha("cancha-1", "2026-11-10")
    calendario.reservar("r-1", "ana", 18, 19)
    consultas = 0
    segundo = 0
    while True:
        if segundo >= SEGUNDO_DE_LA_CANCELACION and not calendario.esta_libre(18, 19):
            calendario.cancelar("r-1")
        consultas = consultas + 1
        if calendario.esta_libre(18, 19):
            return consultas, segundo
        segundo = segundo + intervalo_segundos


# ---------------------------------------------------------------- Parte B

class ObservadorDeCalendario:
    """Lo que el calendario sabe de quien se suscribe: que tiene este metodo."""

    def al_liberarse(self, cancha, franja):
        raise NotImplementedError


class CalendarioObservable(CalendarioDeCancha):
    
    def __init__(self, cancha, fecha):
        super().__init__(cancha, fecha)
        self.observadores = []

    def suscribir(self, observador: ObservadorDeCalendario):
        self.observadores.append(observador)

    def mirame(self, observador: ObservadorDeCalendario):
        """Alias del nombre usado originalmente en el enunciado."""
        self.suscribir(observador)

    def cancelar(self, id_reserva):
        franja = self.franja_de(id_reserva)
        super().cancelar(id_reserva)

        for observador in self.observadores:
            observador.al_liberarse(self.cancha, franja)

class ListaDeEspera(ObservadorDeCalendario):
    def __init__(self, notificador):
        self.notificador = notificador
        self.esperando = {}

    def anotar(self, estudiante, franja):
        if franja not in self.esperando:
            self.esperando[franja] = []
        self.esperando[franja].append(estudiante)

    def al_liberarse(self, cancha, franja):
        if (len(self.esperando.get(franja, [])) == 0):
            return
        
        primero = self.esperando[franja].pop(0)

        notificacion = f"Se libero {cancha} el {franja.fecha} de {franja.inicio} a {franja.fin}"
        
        self.notificador.enviar(primero, notificacion)

if __name__ == "__main__":
    print("Parte A: consultando")
    for intervalo in [30, 300]:
        consultas, segundo = simular_consultas(intervalo)
        print("  Cada", intervalo, "s: beto se entera en el segundo", segundo, "despues de", consultas, "consultas")
    consultas, segundo = simular_consultas(30)
    print("  2000 estudiantes esperando, cada 30 s:", 2000 * consultas, "consultas")

    print("Parte B: con Observer")
    notificador = NotificadorEnMemoria()
    lista = ListaDeEspera(notificador)
    calendario = CalendarioObservable("cancha-1", "2026-11-10")
    calendario.mirame(lista)
    calendario.reservar("r-1", "ana", 18, 19)
    calendario.reservar("r-2", "carla", 9, 10)
    lista.anotar("beto", FranjaHoraria("2026-11-10", 18, 19))
    lista.anotar("dani", FranjaHoraria("2026-11-10", 18, 19))

    calendario.cancelar("r-2")
    calendario.cancelar("r-1")
    for destinatario, texto in notificador.enviados:
        print(" ", destinatario, "<-", texto)
    print("  Siguen esperando 18-19:", lista.esperando[FranjaHoraria("2026-11-10", 18, 19)])
