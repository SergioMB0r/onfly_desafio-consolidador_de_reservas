from datetime import date
from onfly_report.services.stay_calculator import calculate_room_nights

def test_room_nights_with_zero_rooms():
    """Se a reserva tem 0 quartos, as noites devem ser 0, independente das datas"""
    checkin = date(2025, 1, 10)
    checkout = date(2025, 1, 15)

    assert calculate_room_nights(checkin, checkout, rooms=0) ==0