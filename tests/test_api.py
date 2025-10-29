from datetime import datetime
from tests.data import get_base_sailings, get_year_boundary_sailings


def test_get_capacity_success(client):
    """
    Tests the /capacity endpoint with a date range that has data.
    """
    test_client, seed_data = client
    seed_data(get_base_sailings())

    response = test_client.get("/capacity?date_from=2024-01-01&date_to=2024-01-31")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5

    first_week = data[0]
    assert first_week["week_start_date"] == "2024-01-01"
    assert first_week["week_no"] == 1
    assert first_week["offered_capacity_teu"] == 25.0


def test_rolling_average_calculation(client):
    """
    Tests that the 4-week rolling average is calculated correctly.
    """
    test_client, seed_data = client
    seed_data(get_base_sailings())

    response = test_client.get("/capacity?date_from=2024-01-01&date_to=2024-01-29")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

    expected_averages = [25.0, 75.0, 150.0, 250.0, 350.0]
    for i, week in enumerate(data):
        assert week["offered_capacity_teu"] == expected_averages[i]


def test_bad_date_range(client):
    """
    Tests that an invalid date range returns a 400 error.
    """
    test_client, _ = client
    response = test_client.get("/capacity?date_from=2024-03-31&date_to=2024-01-01")
    assert response.status_code == 400
    assert response.json()["detail"] == "date_from cannot be after date_to"


def test_get_capacity_no_data_range(client):
    """
    Tests a date range where no sailing data exists.
    """
    test_client, seed_data = client
    seed_data([])  # make it such that there is no data

    response = test_client.get("/capacity?date_from=2026-01-05&date_to=2026-01-12")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["offered_capacity_teu"] == 0.0
    assert data[1]["offered_capacity_teu"] == 0.0


def test_get_capacity_single_day_range(client):
    """
    Tests a date range that starts and ends on the same day.
    """
    test_client, seed_data = client
    seed_data(get_base_sailings())

    response = test_client.get("/capacity?date_from=2024-01-10&date_to=2024-01-10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["week_start_date"] == "2024-01-08"
    assert data[0]["week_no"] == 2
    assert data[0]["offered_capacity_teu"] == 75.0


def test_invalid_date_format(client):
    """
    Tests that invalid date formats return a 422 validation error.
    """
    test_client, _ = client
    response = test_client.get("/capacity?date_from=invalid-date&date_to=2024-03-31")
    assert response.status_code == 422


def test_missing_parameters(client):
    """
    Tests that missing parameters use default values.
    """
    test_client, seed_data = client
    seed_data(get_base_sailings())

    response = test_client.get("/capacity")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["week_start_date"] == "2024-01-01"
    assert data[0]["offered_capacity_teu"] == 25.0


def test_response_schema_compliance(client):
    """
    Tests that the response schema is compliant.
    """
    test_client, seed_data = client
    seed_data(get_base_sailings())

    response = test_client.get("/capacity?date_from=2024-01-01&date_to=2024-01-08")
    assert response.status_code == 200
    data = response.json()
    for week in data:
        assert "week_start_date" in week
        assert "week_no" in week
        assert "offered_capacity_teu" in week
        assert isinstance(week["week_start_date"], str)
        assert isinstance(week["week_no"], int)
        assert isinstance(week["offered_capacity_teu"], float)
        datetime.strptime(week["week_start_date"], "%Y-%m-%d")


def test_year_boundary(client):
    """
    Tests the API correctly handles a date range that spans a year boundary.
    """
    test_client, seed_data = client
    seed_data(get_year_boundary_sailings())

    response = test_client.get("/capacity?date_from=2023-12-25&date_to=2024-01-01")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    assert data[0]["week_start_date"] == "2023-12-25"
    assert data[0]["week_no"] == 52
    assert data[0]["offered_capacity_teu"] == 150.0

    assert data[1]["week_start_date"] == "2024-01-01"
    assert data[1]["week_no"] == 1
    assert data[1]["offered_capacity_teu"] == 325.0
