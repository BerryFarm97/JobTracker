import sqlite3
import pytest
import database


@pytest.fixture
def isolated_database(tmp_path, monkeypatch):
    database_path = tmp_path / "test_job_tracker.db"
    real_connect = sqlite3.connect

    def connect_to_test_database(_filename):
        return real_connect(database_path)

    monkeypatch.setattr(
        database.sqlite3,
        "connect",
        connect_to_test_database,
    )

    assert database.initialize_database() is True
    return database_path


@pytest.fixture
def sample_application():
    return {
        "company_name": "OpenAI",
        "job_title": "Junior Python Developer",
        "salary_range": "$70,000-$85,000",
        "location": "Remote",
        "notes": "Applied through the company website",
        "status": "Applied",
        "application_date": "2026-07-22",
        "url": "https://example.com/jobs/123",
        "archived": 0,
    }
