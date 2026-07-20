import csv


def convert_db_csv(csv_dictionaries, final_path):
    columns = [
        "Company Name",
        "Job Title",
        "Salary Range",
        "Location",
        "Notes",
        "Status",
        "Application Date",
        "URL",
        "Archived",
    ]

    try:
        with open(
            final_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            applications_writer = csv.DictWriter(
                csv_file,
                fieldnames=columns,
            )
            applications_writer.writeheader()
            applications_writer.writerows(csv_dictionaries)
            return True

    except (
        OSError,
        csv.Error,
    ):
        return False
