from datetime import date
from app.schemas import Sailing


def get_base_sailings():
    return [
        Sailing(
            ORIGIN="china_main",
            DESTINATION="north_europe_main",
            SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS="S1",
            ORIGIN_SERVICE_VERSION_AND_MASTER="M1",
            DESTINATION_SERVICE_VERSION_AND_MASTER="D1",
            ORIGIN_AT_UTC=date(2024, 1, 1),
            OFFERED_CAPACITY_TEU=100,
        ),
        Sailing(
            ORIGIN="china_main",
            DESTINATION="north_europe_main",
            SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS="S2",
            ORIGIN_SERVICE_VERSION_AND_MASTER="M2",
            DESTINATION_SERVICE_VERSION_AND_MASTER="D2",
            ORIGIN_AT_UTC=date(2024, 1, 8),
            OFFERED_CAPACITY_TEU=200,
        ),
        Sailing(
            ORIGIN="china_main",
            DESTINATION="north_europe_main",
            SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS="S3",
            ORIGIN_SERVICE_VERSION_AND_MASTER="M3",
            DESTINATION_SERVICE_VERSION_AND_MASTER="D3",
            ORIGIN_AT_UTC=date(2024, 1, 15),
            OFFERED_CAPACITY_TEU=300,
        ),
        Sailing(
            ORIGIN="china_main",
            DESTINATION="north_europe_main",
            SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS="S4",
            ORIGIN_SERVICE_VERSION_AND_MASTER="M4",
            DESTINATION_SERVICE_VERSION_AND_MASTER="D4",
            ORIGIN_AT_UTC=date(2024, 1, 22),
            OFFERED_CAPACITY_TEU=400,
        ),
        Sailing(
            ORIGIN="china_main",
            DESTINATION="north_europe_main",
            SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS="S5",
            ORIGIN_SERVICE_VERSION_AND_MASTER="M5",
            DESTINATION_SERVICE_VERSION_AND_MASTER="D5",
            ORIGIN_AT_UTC=date(2024, 1, 29),
            OFFERED_CAPACITY_TEU=500,
        ),
    ]


def get_year_boundary_sailings():
    return [
        Sailing(
            ORIGIN="china_main",
            DESTINATION="north_europe_main",
            SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS="S6",
            ORIGIN_SERVICE_VERSION_AND_MASTER="M6",
            DESTINATION_SERVICE_VERSION_AND_MASTER="D6",
            ORIGIN_AT_UTC=date(2023, 12, 25),
            OFFERED_CAPACITY_TEU=600,
        ),
        Sailing(
            ORIGIN="china_main",
            DESTINATION="north_europe_main",
            SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS="S7",
            ORIGIN_SERVICE_VERSION_AND_MASTER="M7",
            DESTINATION_SERVICE_VERSION_AND_MASTER="D7",
            ORIGIN_AT_UTC=date(2024, 1, 1),
            OFFERED_CAPACITY_TEU=700,
        ),
    ]


def get_multi_origin_sailings():
    """I realized that this is not used now, but leaving it here in case of future tests."""
    return [
        # Same week, same origin/destination
        Sailing(
            ORIGIN="china_main",
            DESTINATION="north_europe_main",
            SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS="S1",
            ORIGIN_SERVICE_VERSION_AND_MASTER="M1",
            DESTINATION_SERVICE_VERSION_AND_MASTER="D1",
            ORIGIN_AT_UTC=date(2024, 1, 1),
            OFFERED_CAPACITY_TEU=100,
        ),
        Sailing(
            ORIGIN="china_main",
            DESTINATION="north_europe_main",
            SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS="S2",
            ORIGIN_SERVICE_VERSION_AND_MASTER="M2",
            DESTINATION_SERVICE_VERSION_AND_MASTER="D2",
            ORIGIN_AT_UTC=date(2024, 1, 2),
            OFFERED_CAPACITY_TEU=150,
        ),
        # Different destination
        Sailing(
            ORIGIN="china_main",
            DESTINATION="us_west_coast",
            SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS="S3",
            ORIGIN_SERVICE_VERSION_AND_MASTER="M3",
            DESTINATION_SERVICE_VERSION_AND_MASTER="D3",
            ORIGIN_AT_UTC=date(2024, 1, 1),
            OFFERED_CAPACITY_TEU=1000,
        ),
        # Second week for rolling average calculation
        Sailing(
            ORIGIN="china_main",
            DESTINATION="north_europe_main",
            SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS="S4",
            ORIGIN_SERVICE_VERSION_AND_MASTER="M4",
            DESTINATION_SERVICE_VERSION_AND_MASTER="D4",
            ORIGIN_AT_UTC=date(2024, 1, 8),
            OFFERED_CAPACITY_TEU=250,
        ),
    ]
