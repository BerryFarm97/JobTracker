# Job Tracker

Job Tracker is a command-line application for organizing and tracking job applications. It stores application details in a local SQLite database and provides tools for searching, filtering, updating, archiving, restoring, deleting, and exporting application records.

I built this project to strengthen my Python fundamentals while gaining practical experience with database operations, application structure, input validation, automated testing, and Git/GitHub workflows.

## Features

- Add job applications with required and optional information
- Store application data locally using SQLite
- View active applications
- Sort applications by:
  - Newest
  - Oldest
  - Company name
  - Application status
- Update application details or status
- Search applications by keyword or phrase
- Filter applications by status
- Archive applications without permanently deleting them
- Restore archived applications
- Permanently delete archived applications
- Validate optional application URLs
- Export active, archived, or all applications to CSV
- Prevent existing CSV exports from being overwritten
- Handle invalid input and database failures with clear messages
- Verify core behavior with 15 automated tests

## Technologies Used

- Python
- SQLite
- `pytest`
- Python standard-library modules including:
  - `sqlite3`
  - `csv`
  - `pathlib`
  - `urllib.parse`
  - `datetime`

The application itself uses only the Python standard library. `pytest` is required only for running the automated tests.

## Project Structure

```text
JobTracker/
├── main.py
├── database.py
├── csv_exporter.py
├── tests/
│   ├── conftest.py
│   ├── test_csv_exporter.py
│   ├── test_database.py
│   ├── test_input_handlers.py
│   └── test_url_validation.py
├── .gitignore
├── LICENSE
└── README.md
```

### Main Files

- `main.py` contains the command-line menus, input handling, validation, and application workflows.
- `database.py` contains the SQLite queries and database operations.
- `csv_exporter.py` handles writing application data to CSV files.
- `tests/` contains the automated test suite.

## Getting Started

### Requirements

- Python 3 installed
- Git, if cloning the repository
- `pytest`, if running the tests

This project was developed and tested using Python 3.13.

### Clone the Repository

```bash
git clone https://github.com/BerryFarm97/JobTracker.git
cd JobTracker
```

### Run the Application

On Windows:

```powershell
py main.py
```

On macOS or Linux:

```bash
python3 main.py
```

The SQLite database is created automatically the first time the application runs.

## Application Menu

```text
1. Add a job
2. View Applications
3. Update Application
4. Archive Application
5. View Archived Applications
6. Filter Applications By Status
7. Search for applications
8. Convert Table to CSV
9. Exit
```

## CSV Export

Applications can be exported using one of three options:

- Active applications only
- Archived applications only
- All applications

The exported CSV excludes the internal database ID and displays the archived value as `Yes` or `No`.

If no destination is entered, the file is saved in the project folder as:

```text
applications_table.csv
```

If that filename already exists, the application creates a new filename such as:

```text
applications_table(1).csv
applications_table(2).csv
```

This prevents previous exports from being overwritten.

## Running the Tests

Install `pytest` if it is not already installed:

```powershell
py -m pip install pytest
```

Run the complete test suite:

```powershell
py -m pytest -v
```

The test suite currently contains 15 tests covering:

- Numeric menu input
- Retrying after invalid input
- URL validation
- Adding and retrieving applications
- Updating application details and statuses
- Protection against untrusted database columns
- Filtering and keyword searching
- Archiving and restoring applications
- Permanent deletion rules
- CSV database queries
- CSV file creation and failure handling

Database tests use an isolated temporary database so the real `job_tracker.db` file is never modified during testing.

## Important Implementation Details

- SQL values are passed using parameterized queries.
- Editable database columns are restricted through an allowlist.
- Application data persists between program sessions.
- Archived applications are excluded from active searches and filters.
- Only archived applications can be permanently deleted.
- URLs must use either `http://` or `https://` and contain a hostname.
- Database functions return consistent success or failure results.
- SQLite connections are closed after every operation, including failures.

## What I Learned

This project gave me experience turning a small program into a more complete and maintainable application. I worked through database schema changes, validation, error handling, application refactoring, CSV generation, and automated testing.

I also gained practical experience using feature branches, pull requests, commits, and code reviews instead of treating GitHub as simple file storage.

## Project Status

Job Tracker `v1.0.0` is feature-complete.

## Author

Austin Granbery

GitHub: [BerryFarm97](https://github.com/BerryFarm97)

## License

This project is available under the [MIT License](LICENSE).
