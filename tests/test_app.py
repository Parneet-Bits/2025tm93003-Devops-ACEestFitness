"""Functional tests for ACEest's Flask routes and client validation."""
import sqlite3

import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    database = tmp_path / "test_aceest.db"
    test_app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-key",
        "DATABASE_PATH": str(database),
    })
    yield test_app


@pytest.fixture()
def client(app):
    return app.test_client()


def valid_client_form(**overrides):
    payload = {
        "name": "Aarav Mehta",
        "age": "26",
        "weight": "72",
        "program": "Fat Loss (FL) – 3 day",
        "adherence": "75",
    }
    payload.update(overrides)
    return payload


def test_homepage_returns_dashboard_and_all_programmes(client):
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "ACEest" in html
    assert "Fat Loss (FL) – 3 day" in html
    assert "Muscle Gain (MG) – PPL" in html
    assert "Beginner (BG)" in html
    assert "Client directory" in html


def test_health_endpoint_reports_ok(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json() == {"service": "aceest-fitness", "status": "ok"}


def test_programme_api_returns_four_programmes(client):
    response = client.get("/api/programs")
    assert response.status_code == 200
    payload = response.get_json()["programs"]
    assert len(payload) == 4
    assert payload[0]["name"] == "Fat Loss (FL) – 3 day"
    assert payload[0]["workout"]
    assert payload[0]["nutrition"]


def test_client_api_returns_saved_client(client):
    client.post("/clients", data=valid_client_form())
    response = client.get("/api/clients")
    assert response.status_code == 200
    record = response.get_json()["clients"][0]
    assert record["name"] == "Aarav Mehta"
    assert record["calories"] == 1584


def test_can_add_client_and_calculates_estimate(client, app):
    response = client.post("/clients", data=valid_client_form(), follow_redirects=True)
    assert response.status_code == 200
    assert "Aarav Mehta was added successfully." in response.get_data(as_text=True)
    assert "Aarav Mehta" in response.get_data(as_text=True)
    with sqlite3.connect(app.config["DATABASE_PATH"]) as db:
        row = db.execute("SELECT age, weight, program, calories, adherence FROM clients").fetchone()
    assert row == (26, 72.0, "Fat Loss (FL) – 3 day", 1584, 75)


def test_calorie_factor_changes_with_selected_program(client, app):
    client.post("/clients", data=valid_client_form(
        name="Mira Rao", program="Muscle Gain (MG) – PPL", weight="60", adherence="90"
    ))
    with sqlite3.connect(app.config["DATABASE_PATH"]) as db:
        calories = db.execute("SELECT calories FROM clients WHERE name = ?", ("Mira Rao",)).fetchone()[0]
    assert calories == 2100


@pytest.mark.parametrize("payload, expected_message", [
    ({"name": "", "age": "26", "weight": "72", "program": "Beginner (BG)", "adherence": "70"}, "Client name is required."),
    ({"name": "Invalid Age", "age": "15", "weight": "72", "program": "Beginner (BG)", "adherence": "70"}, "Age must be between 16 and 100."),
    ({"name": "Invalid Weight", "age": "26", "weight": "0", "program": "Beginner (BG)", "adherence": "70"}, "Weight must be between 20 and 350 kg."),
    ({"name": "Invalid Program", "age": "26", "weight": "72", "program": "Hacker Plan", "adherence": "70"}, "Select a valid fitness programme."),
    ({"name": "Invalid Adherence", "age": "26", "weight": "72", "program": "Beginner (BG)", "adherence": "101"}, "Adherence must be between 0 and 100 percent."),
])
def test_invalid_client_input_is_rejected(client, payload, expected_message):
    response = client.post("/clients", data=payload, follow_redirects=True)
    assert response.status_code == 200
    assert expected_message in response.get_data(as_text=True)


def test_duplicate_client_name_is_rejected_case_insensitively(client):
    client.post("/clients", data=valid_client_form())
    response = client.post("/clients", data=valid_client_form(name="aarav mehta"), follow_redirects=True)
    assert "A client with that name already exists" in response.get_data(as_text=True)
    assert response.get_data(as_text=True).count("Aarav Mehta") >= 1


def test_delete_client(client, app):
    client.post("/clients", data=valid_client_form())
    with sqlite3.connect(app.config["DATABASE_PATH"]) as db:
        client_id = db.execute("SELECT id FROM clients WHERE name = ?", ("Aarav Mehta",)).fetchone()[0]
    response = client.post(f"/clients/{client_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    assert "Client removed successfully." in response.get_data(as_text=True)
    with sqlite3.connect(app.config["DATABASE_PATH"]) as db:
        assert db.execute("SELECT count(*) FROM clients").fetchone()[0] == 0


def test_client_name_is_stored_as_text_not_executed_as_sql(client, app):
    unusual_name = "' OR 1=1 --"
    response = client.post("/clients", data=valid_client_form(name=unusual_name), follow_redirects=True)
    assert response.status_code == 200
    with sqlite3.connect(app.config["DATABASE_PATH"]) as db:
        row = db.execute("SELECT name FROM clients").fetchone()
    assert row == (unusual_name,)
