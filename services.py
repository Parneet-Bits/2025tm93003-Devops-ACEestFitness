"""Business rules kept independent from Flask so they are easy to unit test."""
from __future__ import annotations

from typing import Any

PROGRAMS: dict[str, dict[str, Any]] = {
    "Fat Loss (FL) – 3 day": {
        "factor": 22,
        "category": "FAT LOSS",
        "description": "A balanced three-day full-body routine with recovery between sessions.",
        "workout": ["Day 1 · Full-body strength", "Day 2 · Cardio + core", "Day 3 · Full-body strength"],
        "nutrition": "Prioritise balanced meals, vegetables, protein sources and hydration.",
    },
    "Fat Loss (FL) – 5 day": {
        "factor": 24,
        "category": "FAT LOSS",
        "description": "A five-day plan combining strength training and conditioning.",
        "workout": ["Mon · Lower body", "Tue · Cardio + core", "Wed · Upper body", "Thu · Conditioning", "Fri · Full body"],
        "nutrition": "Build meals around protein, fibre-rich carbohydrates and vegetables.",
    },
    "Muscle Gain (MG) – PPL": {
        "factor": 35,
        "category": "MUSCLE GAIN",
        "description": "A push / pull / legs split for progressive strength training.",
        "workout": ["Day 1 · Push", "Day 2 · Pull", "Day 3 · Legs", "Repeat with planned recovery"],
        "nutrition": "Eat regular balanced meals with adequate protein and energy for training.",
    },
    "Beginner (BG)": {
        "factor": 26,
        "category": "BEGINNER",
        "description": "A beginner-friendly plan focused on technique and consistency.",
        "workout": ["Air squats", "Incline push-ups", "Rows", "Walking + mobility"],
        "nutrition": "Start with balanced meals and consistent hydration; build habits gradually.",
    },
}


def calculate_estimated_calories(weight_kg: float, program: str) -> int:
    """Return the simple multiplier-based estimate used in the supplied ACEest versions."""
    if program not in PROGRAMS:
        raise ValueError("Unknown fitness programme.")
    if not 20 <= float(weight_kg) <= 350:
        raise ValueError("Weight must be between 20 and 350 kg.")
    return round(float(weight_kg) * PROGRAMS[program]["factor"])


def validate_client_data(
    name: str,
    raw_age: str,
    raw_weight: str,
    program: str,
    raw_adherence: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    """Validate raw form values and return a normalised record plus readable errors."""
    name = (name or "").strip()
    errors: list[str] = []
    if not name:
        errors.append("Client name is required.")
    if len(name) > 80:
        errors.append("Client name must be 80 characters or fewer.")

    try:
        age = int(raw_age)
        if not 16 <= age <= 100:
            errors.append("Age must be between 16 and 100.")
    except (TypeError, ValueError):
        age = 0
        errors.append("Enter a valid whole-number age.")

    try:
        weight = float(raw_weight)
        if not 20 <= weight <= 350:
            errors.append("Weight must be between 20 and 350 kg.")
    except (TypeError, ValueError):
        weight = 0.0
        errors.append("Enter a valid weight in kilograms.")

    if program not in PROGRAMS:
        errors.append("Select a valid fitness programme.")

    try:
        adherence = int(raw_adherence)
        if not 0 <= adherence <= 100:
            errors.append("Adherence must be between 0 and 100 percent.")
    except (TypeError, ValueError):
        adherence = -1
        errors.append("Enter a valid adherence percentage.")

    if errors:
        return None, errors
    return {
        "name": name,
        "age": age,
        "weight": weight,
        "program": program,
        "adherence": adherence,
    }, []
