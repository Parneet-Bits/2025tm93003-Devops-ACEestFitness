"""Unit tests for programme calculations and form validation (no web server needed)."""
import pytest

from services import PROGRAMS, calculate_estimated_calories, validate_client_data


def test_calorie_estimate_matches_supplied_aceest_multiplier():
    assert calculate_estimated_calories(72, "Fat Loss (FL) – 3 day") == 1584
    assert calculate_estimated_calories(60, "Muscle Gain (MG) – PPL") == 2100


@pytest.mark.parametrize("program, factor", [
    ("Fat Loss (FL) – 3 day", 22),
    ("Fat Loss (FL) – 5 day", 24),
    ("Muscle Gain (MG) – PPL", 35),
    ("Beginner (BG)", 26),
])
def test_all_programmes_have_expected_factor(program, factor):
    assert PROGRAMS[program]["factor"] == factor
    assert calculate_estimated_calories(50, program) == 50 * factor


def test_unknown_program_is_rejected_by_calculator():
    with pytest.raises(ValueError, match="Unknown fitness programme"):
        calculate_estimated_calories(60, "No Such Plan")


def test_valid_form_is_normalised():
    record, errors = validate_client_data("  Mira Rao  ", "28", "61.5", "Beginner (BG)", "100")
    assert errors == []
    assert record == {
        "name": "Mira Rao", "age": 28, "weight": 61.5,
        "program": "Beginner (BG)", "adherence": 100,
    }


@pytest.mark.parametrize("age, expected", [
    ("15", "Age must be between 16 and 100."),
    ("101", "Age must be between 16 and 100."),
    ("not-a-number", "Enter a valid whole-number age."),
])
def test_age_validation(age, expected):
    record, errors = validate_client_data("Riya", age, "60", "Beginner (BG)", "75")
    assert record is None and expected in errors


@pytest.mark.parametrize("weight, expected", [
    ("19.9", "Weight must be between 20 and 350 kg."),
    ("351", "Weight must be between 20 and 350 kg."),
    ("heavy", "Enter a valid weight in kilograms."),
])
def test_weight_validation(weight, expected):
    record, errors = validate_client_data("Riya", "26", weight, "Beginner (BG)", "75")
    assert record is None and expected in errors


@pytest.mark.parametrize("adherence, expected", [
    ("-1", "Adherence must be between 0 and 100 percent."),
    ("101", "Adherence must be between 0 and 100 percent."),
    ("many", "Enter a valid adherence percentage."),
])
def test_adherence_validation(adherence, expected):
    record, errors = validate_client_data("Riya", "26", "60", "Beginner (BG)", adherence)
    assert record is None and expected in errors


def test_name_and_program_validation():
    record, errors = validate_client_data("  ", "26", "60", "Unknown", "50")
    assert record is None
    assert "Client name is required." in errors
    assert "Select a valid fitness programme." in errors


def test_name_length_is_limited():
    record, errors = validate_client_data("x" * 81, "26", "60", "Beginner (BG)", "50")
    assert record is None
    assert "Client name must be 80 characters or fewer." in errors
