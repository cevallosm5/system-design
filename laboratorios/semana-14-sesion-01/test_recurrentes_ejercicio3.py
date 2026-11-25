"""Pruebas del Ejercicio 3: las escriben ustedes, en pareja, una a la vez."""

import pytest

from recurrentes_ejercicio3 import AgendaDeCancha


def test_calendario_crea_un_agregado_por_fecha():
    agenda = AgendaDeCancha("norte")

    calendario = agenda.calendario("2026-11-16")

    assert calendario.cancha == "norte"
    assert calendario.fecha == "2026-11-16"
    assert agenda.calendario("2026-11-16") is calendario


def test_reserva_la_franja_en_varias_semana_con_ids_secuenciales():
    agenda = AgendaDeCancha("norte")

    resultados = agenda.reservar_cada_semana(
        "entreno", "ana", "2026-11-16", 18, 19, 3
    )

    assert resultados == [
        ("2026-11-16", "reservada"),
        ("2026-11-23", "reservada"),
        ("2026-11-30", "reservada"),
    ]
    assert agenda.calendario("2026-11-16").reservas()[0][0] == "entreno-1"
    assert agenda.calendario("2026-11-23").reservas()[0][0] == "entreno-2"


@pytest.mark.parametrize("semanas", [0, 13, -1])
def test_rechaza_cantidad_de_semanas_fuera_del_rango(semanas):
    agenda = AgendaDeCancha("norte")

    with pytest.raises(ValueError):
        agenda.reservar_cada_semana(
            "entreno", "ana", "2026-11-16", 18, 19, semanas
        )

    assert agenda._calendarios == {}


def test_semana_ocupada_se_salta_y_las_siguientes_continuan():
    agenda = AgendaDeCancha("norte")
    agenda.calendario("2026-11-23").reservar(
        "ocupada", "beto", 18, 19
    )

    resultados = agenda.reservar_cada_semana(
        "entreno", "ana", "2026-11-16", 18, 19, 3
    )

    assert resultados == [
        ("2026-11-16", "reservada"),
        ("2026-11-23", "ocupada"),
        ("2026-11-30", "reservada"),
    ]


def test_franja_que_excede_dos_horas_se_reporta_como_limite():
    agenda = AgendaDeCancha("norte")
    agenda.calendario("2026-11-16").reservar(
        "previa", "ana", 18, 19
    )

    resultados = agenda.reservar_cada_semana(
        "entreno", "ana", "2026-11-16", 19, 21, 2
    )

    assert resultados == [
        ("2026-11-16", "limite"),
        ("2026-11-23", "reservada"),
    ]
