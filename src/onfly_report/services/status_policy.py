"""Política de status das reservas."""

from __future__ import annotations



def is_billable(status: str) -> bool:
    if status != "CONFIRMED":
        return False
    return True