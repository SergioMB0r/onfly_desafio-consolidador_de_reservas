"""Cálculo de noites ocupadas."""

from __future__ import annotations

from datetime import date



def calculate_room_nights(checkin: date, checkout: date, rooms: int) -> int:
    if checkout <= checkin:
        return 0

    nights = (checkout - checkin).days
    return nights * rooms