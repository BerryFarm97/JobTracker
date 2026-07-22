import pytest
import database


def test_adds_and_retrieves_active_application(
    isolated_database,
    sample_application,
):
    assert database.add_application(sample_application) is True

    applications = database.get_active_applications("Newest")

    assert len(applications) == 1
    assert applications[0]["company_name"] == "OpenAI"
    assert applications[0]["job_title"] == "Junior Python Developer"
    assert applications[0]["archived"] == 0


def test_updates_status_and_editable_value(
    isolated_database,
    sample_application,
):
    assert database.add_application(sample_application) is True

    application_id = database.get_active_applications("Newest")[0]["id"]

    assert (
        database.update_status(
            application_id,
            "Interviewing",
        )
        is True
    )

    assert (
        database.edit_application_values(
            application_id,
            "notes",
            "Phone interview scheduled",
        )
        is True
    )

    updated = database.get_active_applications("Newest")[0]

    assert updated["status"] == "Interviewing"
    assert updated["notes"] == "Phone interview scheduled"


def test_rejects_untrusted_edit_column(
    isolated_database,
    sample_application,
):
    assert database.add_application(sample_application) is True

    application_id = database.get_active_applications("Newest")[0]["id"]

    result = database.edit_application_values(
        application_id,
        "archived = 1",
        "bad value",
    )

    assert result is False
    assert database.get_active_applications("Newest")[0]["archived"] == 0


def test_filters_and_searches_only_active_applications(
    isolated_database,
    sample_application,
):
    second_application = sample_application.copy()
    second_application.update(
        {
            "company_name": "Blue Origin",
            "job_title": "Software Engineer",
            "notes": "Work on lunar systems",
            "status": "Interviewing",
            "application_date": "2026-07-21",
        }
    )

    assert database.add_application(sample_application) is True
    assert database.add_application(second_application) is True

    filtered = database.get_filtered_applications(
        "Interviewing",
        "Company Name",
    )

    search_results = database.get_search_results(
        "lunar",
        "Newest",
    )

    assert len(filtered) == 1
    assert filtered[0]["company_name"] == "Blue Origin"

    assert len(search_results) == 1
    assert search_results[0]["company_name"] == "Blue Origin"

    blue_origin_id = filtered[0]["id"]

    assert (
        database.archive_application_by_id(
            blue_origin_id,
        )
        is True
    )

    assert (
        database.get_filtered_applications(
            "Interviewing",
            "Newest",
        )
        == []
    )

    assert (
        database.get_search_results(
            "lunar",
            "Newest",
        )
        == []
    )


def test_archives_restores_and_permanently_deletes_application(
    isolated_database,
    sample_application,
):
    assert database.add_application(sample_application) is True

    application_id = database.get_active_applications("Newest")[0]["id"]

    assert database.archive_application_by_id(application_id) is True
    assert database.get_active_applications("Newest") == []
    assert len(database.get_archived("Newest")) == 1

    assert database.restore_application_by_id(application_id) is True
    assert len(database.get_active_applications("Newest")) == 1
    assert database.get_archived("Newest") == []

    # Active applications cannot be permanently deleted.
    assert database.delete_archived_app(application_id) is False

    assert database.archive_application_by_id(application_id) is True
    assert database.delete_archived_app(application_id) is True

    assert database.get_active_applications("Newest") == []
    assert database.get_archived("Newest") == []


def test_csv_data_filters_rows_and_formats_archived_value(
    isolated_database,
    sample_application,
):
    archived_application = sample_application.copy()
    archived_application.update(
        {
            "company_name": "NASA",
            "job_title": "Application Developer",
            "archived": 1,
        }
    )

    assert database.add_application(sample_application) is True
    assert database.add_application(archived_application) is True

    active_rows = database.get_csv_data("active")
    archived_rows = database.get_csv_data("archived")
    all_rows = database.get_csv_data("all")

    assert len(active_rows) == 1
    assert active_rows[0]["Company Name"] == "OpenAI"
    assert active_rows[0]["Archived"] == "No"

    assert len(archived_rows) == 1
    assert archived_rows[0]["Company Name"] == "NASA"
    assert archived_rows[0]["Archived"] == "Yes"

    assert len(all_rows) == 2
    assert "id" not in all_rows[0].keys()


def test_rejects_unknown_csv_filter(isolated_database):
    with pytest.raises(ValueError):
        database.get_csv_data("unknown")
