"""ACEest Fitness & Gym - Flask application for the DevOps assignment."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, flash, g, jsonify, redirect, render_template, request, url_for

from services import PROGRAMS, calculate_estimated_calories, validate_client_data


SCHEMA = """
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL COLLATE NOCASE UNIQUE,
    age INTEGER NOT NULL CHECK (age BETWEEN 16 AND 100),
    weight REAL NOT NULL CHECK (weight BETWEEN 20 AND 350),
    program TEXT NOT NULL,
    calories INTEGER NOT NULL,
    adherence INTEGER NOT NULL CHECK (adherence BETWEEN 0 AND 100),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Create a configured Flask application (also used by pytest)."""
    app = Flask(__name__)
    default_db = Path(app.instance_path) / "aceest_fitness.db"
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "local-dev-key-change-before-deployment"),
        DATABASE_PATH=os.environ.get("DATABASE_PATH", str(default_db)),
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)

    db_path = app.config["DATABASE_PATH"]
    if db_path != ":memory:":
        Path(db_path).expanduser().parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.execute(SCHEMA)

    def get_db() -> sqlite3.Connection:
        if "db" not in g:
            connection = sqlite3.connect(app.config["DATABASE_PATH"])
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            g.db = connection
        return g.db

    @app.teardown_appcontext
    def close_db(_error: BaseException | None = None) -> None:
        connection = g.pop("db", None)
        if connection is not None:
            connection.close()

    app.get_db = get_db  # type: ignore[attr-defined]
    app.programs = PROGRAMS  # type: ignore[attr-defined]

    @app.get("/")
    def index():
        db = get_db()
        clients = db.execute(
            "SELECT id, name, age, weight, program, calories, adherence, created_at "
            "FROM clients ORDER BY id DESC"
        ).fetchall()
        total_clients = len(clients)
        average_adherence = round(sum(row["adherence"] for row in clients) / total_clients) if total_clients else 0
        return render_template(
            "index.html",
            programs=PROGRAMS,
            clients=clients,
            total_clients=total_clients,
            average_adherence=average_adherence,
            program_count=len(PROGRAMS),
        )

    @app.post("/clients")
    def add_client():
        record, errors = validate_client_data(
            request.form.get("name", ""),
            request.form.get("age", "").strip(),
            request.form.get("weight", "").strip(),
            request.form.get("program", "").strip(),
            request.form.get("adherence", "75").strip(),
        )
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("index") + "#add-client")

        assert record is not None  # validation returns a record when there are no errors
        calories = calculate_estimated_calories(record["weight"], record["program"])
        db = get_db()
        try:
            db.execute(
                "INSERT INTO clients (name, age, weight, program, calories, adherence) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (record["name"], record["age"], record["weight"], record["program"], calories, record["adherence"]),
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("A client with that name already exists. Use a unique name.", "error")
            return redirect(url_for("index") + "#add-client")

        flash(f"{record['name']} was added successfully.", "success")
        return redirect(url_for("index") + "#clients")

    @app.post("/clients/<int:client_id>/delete")
    def delete_client(client_id: int):
        db = get_db()
        cursor = db.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        db.commit()
        if cursor.rowcount:
            flash("Client removed successfully.", "success")
        else:
            flash("Client was not found.", "error")
        return redirect(url_for("index") + "#clients")

    @app.get("/api/programs")
    def api_programs():
        """Expose the programme catalogue for integrations and health checks."""
        return jsonify(programs=[{"name": name, **details} for name, details in PROGRAMS.items()])

    @app.get("/api/clients")
    def api_clients():
        """Expose saved local client rows as JSON for assignment API validation."""
        rows = get_db().execute(
            "SELECT id, name, age, weight, program, calories, adherence, created_at "
            "FROM clients ORDER BY id DESC"
        ).fetchall()
        return jsonify(clients=[dict(row) for row in rows])

    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok", service="aceest-fitness")

    return app


app = create_app()

if __name__ == "__main__":
    # Use Flask's development server for local assignment work only.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
