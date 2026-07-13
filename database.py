import sqlite3


def initialize_database():
    conn = sqlite3.connect("job_tracker.db")

    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS applications(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        company_name TEXT, 
        job_title TEXT, 
        salary_range TEXT, 
        location TEXT, 
        notes TEXT, 
        status TEXT,
        application_date TEXT, 
        archived INTEGER NOT NULL DEFAULT 0)"""
    )

    conn.commit()
    conn.close()


def add_application(application):
    conn = sqlite3.connect("job_tracker.db")

    cur = conn.cursor()

    cur.execute("""INSERT INTO applications
    (company_name, job_title, salary_range, location, notes, status, application_date, archived)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            application['company_name'],
            application['job_title'],
            application['salary_range'],
            application['location'],
            application['notes'],
            application['status'],
            application['application_date'],
            application['archived']

        )
    )


    conn.commit()
    conn.close()


def get_active_applications():
    conn = sqlite3.connect("job_tracker.db")

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""SELECT * FROM applications WHERE archived = 0""")
    applications = cur.fetchall()

    conn.close()

    return applications


def update_status(application_id, new_status):
    conn = sqlite3.connect("job_tracker.db")

    cur = conn.cursor()

    cur.execute(
        """UPDATE applications
            SET status = ?
            WHERE id = ?""",
            (new_status, application_id)
    )

    conn.commit()
    conn.close()


def archived_status(application_id):
    conn = sqlite3.connect("job_tracker.db")
    
    cur = conn.cursor()

    cur.execute(
        """UPDATE applications
            SET archived = 1
            WHERE id = ?""",
            (application_id,)
    )

    conn.commit()
    conn.close()


def get_archived():
    conn = sqlite3.connect("job_tracker.db")

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""SELECT * FROM applications WHERE archived = 1""")
    applications = cur.fetchall()

    conn.close()
    return applications


def change_archive_status(application_id):
    conn = sqlite3.connect("job_tracker.db")

    cur = conn.cursor()

    cur.execute(
        """UPDATE applications
            SET archived = 0
            WHERE id = ?""",
            (application_id,)
    )

    conn.commit()
    conn.close()