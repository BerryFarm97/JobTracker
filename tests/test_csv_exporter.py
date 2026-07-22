import csv
from csv_exporter import convert_db_csv


def test_writes_expected_csv_file(tmp_path):
    applications = [
        {
            "Company Name": "OpenAI",
            "Job Title": "Junior Python Developer",
            "Salary Range": "$70,000-$85,000",
            "Location": "Remote",
            "Notes": "Phone screen scheduled",
            "Status": "Interviewing",
            "Application Date": "2026-07-22",
            "URL": "https://example.com/jobs/123",
            "Archived": "No",
        }
    ]

    output_path = tmp_path / "applications_table.csv"

    assert convert_db_csv(applications, output_path) is True

    with output_path.open(
        newline="",
        encoding="utf-8",
    ) as csv_file:
        reader = csv.DictReader(csv_file)
        exported_rows = list(reader)

    assert reader.fieldnames == list(applications[0].keys())
    assert exported_rows == applications


def test_returns_false_when_csv_cannot_be_created(tmp_path):
    missing_folder_path = tmp_path / "missing-folder" / "applications.csv"

    assert convert_db_csv([], missing_folder_path) is False
