import sqlite3


def initialize_database():
    conn = None

    try:
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
            url TEXT,
            archived INTEGER NOT NULL DEFAULT 0)""")

        conn.commit()
        return True

    except sqlite3.Error:
        if conn is not None:
            conn.rollback()
        return False
    finally:
        if conn is not None:
            conn.close()


def initialize_conn():
    conn = sqlite3.connect("job_tracker.db")
    return conn


def initialize_cur(conn):
    return conn.cursor()


def add_application(application):
    conn = None

    try:
        conn = initialize_conn()

        cur = initialize_cur(conn)

        cur.execute(
            """INSERT INTO applications
        (company_name, job_title, salary_range, location, notes, status, application_date, url, archived)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                application["company_name"],
                application["job_title"],
                application["salary_range"],
                application["location"],
                application["notes"],
                application["status"],
                application["application_date"],
                application["url"],
                application["archived"],
            ),
        )

        if cur.rowcount == 1:
            conn.commit()
            return True
        else:
            conn.rollback()
            return False

    except sqlite3.Error:
        if conn is not None:
            conn.rollback()
        return False

    finally:
        if conn is not None:
            conn.close()


def get_active_applications(sort_choice):
    conn = None

    try:
        conn = initialize_conn()
        conn.row_factory = sqlite3.Row

        cur = initialize_cur(conn)

        sort_options = {
            "Newest": "application_date DESC",
            "Oldest": "application_date ASC",
            "Company Name": "company_name ASC",
            "Application Status": "status ASC",
        }

        order_by = sort_options[sort_choice]

        cur.execute(f"""SELECT *
                    FROM applications
                    WHERE archived = 0
                    ORDER BY {order_by}""")
        applications = cur.fetchall()

        if applications:
            return applications

        elif applications == []:
            return []

    except sqlite3.Error:
        return None

    finally:
        if conn is not None:
            conn.close()


def update_status(application_id, new_status):
    conn = None

    try:

        conn = initialize_conn()
        cur = initialize_cur(conn)

        cur.execute(
            """UPDATE applications
                SET status = ?
                WHERE id = ?""",
            (new_status, application_id),
        )

        if cur.rowcount == 1:
            conn.commit()
            return True

        else:
            conn.rollback()
            return False

    except sqlite3.Error:
        if conn is not None:
            conn.rollback()
        return False

    finally:
        if conn is not None:
            conn.close()


def archived_status(application_id):
    conn = None

    try:
        conn = initialize_conn()

        cur = initialize_cur(conn)

        cur.execute(
            """UPDATE applications
                SET archived = 1
                WHERE id = ?""",
            (application_id,),
        )

        if cur.rowcount == 1:
            conn.commit()
            return True
        else:
            conn.rollback()
            return False

    except sqlite3.Error:
        if conn is not None:
            conn.rollback()
        return False

    finally:
        if conn is not None:
            conn.close()


def edit_application_values(application_id, selected_column, updated_application_value):
    conn = None

    try:
        conn = initialize_conn()

        cur = initialize_cur(conn)

        trusted_columns = [
            "company_name",
            "job_title",
            "salary_range",
            "location",
            "notes",
            "url",
        ]
        if selected_column not in trusted_columns:
            return False

        cur.execute(
            f"""UPDATE applications
                    SET {selected_column} = ?
                    WHERE id = ?""",
            (updated_application_value, application_id),
        )

        if cur.rowcount == 1:
            conn.commit()
            return True
        else:
            conn.rollback()
            return False

    except sqlite3.Error:
        if conn is not None:
            conn.rollback()
        return False
    finally:
        if conn is not None:
            conn.close()


def get_archived(sort_choice):
    conn = None

    try:
        conn = initialize_conn()
        conn.row_factory = sqlite3.Row

        cur = initialize_cur(conn)

        sort_options = {
            "Newest": "application_date DESC",
            "Oldest": "application_date ASC",
            "Company Name": "company_name ASC",
            "Application Status": "status ASC",
        }

        order_by = sort_options[sort_choice]

        cur.execute(f"""SELECT *
                    FROM applications
                    WHERE archived = 1
                    ORDER BY {order_by}""")
        applications = cur.fetchall()

        if applications:
            return applications

        elif applications == []:
            return []

    except sqlite3.Error:
        return None

    finally:
        if conn is not None:
            conn.close()


def change_archive_status(application_id):
    conn = None

    try:
        conn = initialize_conn()

        cur = initialize_cur(conn)

        cur.execute(
            """UPDATE applications
                SET archived = 0
                WHERE id = ?""",
            (application_id,),
        )

        if cur.rowcount == 1:
            conn.commit()
            return True
        else:
            conn.rollback()
            return False

    except sqlite3.Error:
        if conn is not None:
            conn.rollback()
        return False
    finally:
        if conn is not None:
            conn.close()


def return_filtered_apps(status, sort_choice):
    conn = None

    try:
        conn = initialize_conn()
        conn.row_factory = sqlite3.Row

        cur = initialize_cur(conn)

        sort_options = {
            "Newest": "application_date DESC",
            "Oldest": "application_date ASC",
            "Company Name": "company_name ASC",
            "Application Status": "status ASC",
        }

        order_by = sort_options[sort_choice]

        cur.execute(
            f"""SELECT *
                    FROM applications
                    WHERE archived = 0
                    AND
                    status = ?
                    ORDER BY {order_by}""",
            (status,),
        )
        filtered_apps = cur.fetchall()

        if filtered_apps:
            return filtered_apps

        elif filtered_apps == []:
            return []

    except sqlite3.Error:
        return None

    finally:
        if conn is not None:
            conn.close()


def get_search_results(keyword, sort_choice):
    conn = None

    try:
        conn = initialize_conn()
        conn.row_factory = sqlite3.Row

        cur = initialize_cur(conn)

        sort_options = {
            "Newest": "application_date DESC",
            "Oldest": "application_date ASC",
            "Company Name": "company_name ASC",
            "Application Status": "status ASC",
        }

        order_by = sort_options[sort_choice]

        search_pattern = f"%{keyword}%"

        cur.execute(
            f"""SELECT *
                    FROM applications
                    WHERE archived = 0
                    AND (
                    company_name LIKE ?
                    OR job_title LIKE ?
                    OR salary_range LIKE ?
                    OR location LIKE ?
                    OR notes LIKE ?)
                    ORDER BY {order_by}""",
            (
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern,
            ),
        )
        search_results = cur.fetchall()

        if search_results:
            return search_results

        elif search_results == []:
            return []

    except sqlite3.Error:
        return None

    finally:
        if conn is not None:
            conn.close()


def delete_archived_app(app_id):
    conn = None

    try:
        conn = initialize_conn()

        cur = initialize_cur(conn)

        cur.execute(
            """DELETE FROM applications
                    WHERE archived = 1
                    AND id = ?""",
            (app_id,),
        )

        if cur.rowcount == 1:
            conn.commit()
            return True
        else:
            conn.rollback()
            return False

    except sqlite3.Error:
        if conn is not None:
            conn.rollback()
        return False
    finally:
        if conn is not None:
            conn.close()


def get_csv_data(filtered_type):
    conn = None

    try:
        conn = initialize_conn()
        conn.row_factory = sqlite3.Row

        cur = initialize_cur(conn)
        if filtered_type == "active":
            cur.execute("""
                SELECT company_name AS "Company Name",
                job_title AS "Job Title", salary_range AS "Salary Range",
                location AS "Location", notes AS "Notes",
                status AS "Status", application_date AS "Application Date",
                url AS "URL",
                CASE
                    WHEN archived = 1 THEN 'Yes'
                    ELSE 'No'
                END AS "Archived"
                FROM applications
                WHERE archived = 0
                """)

        elif filtered_type == "archived":
            cur.execute("""
                SELECT company_name AS "Company Name",
                job_title AS "Job Title", salary_range AS "Salary Range",
                location AS "Location", notes AS "Notes",
                status AS "Status", application_date AS "Application Date",
                url AS "URL",
                CASE
                    WHEN archived = 1 THEN 'Yes'
                    ELSE 'No'
                END AS "Archived"
                FROM applications
                WHERE archived = 1
                """)

        elif filtered_type == "all":
            cur.execute("""
                SELECT company_name AS "Company Name",
                job_title AS "Job Title", salary_range AS "Salary Range",
                location AS "Location", notes AS "Notes",
                status AS "Status", application_date AS "Application Date",
                url AS "URL",
                CASE
                    WHEN archived = 1 THEN 'Yes'
                    ELSE 'No'
                END AS "Archived"
                FROM applications
                """)

        else:
            raise ValueError("Invalid CSV filter type")

        csv_rows = cur.fetchall()
        return csv_rows

    except sqlite3.Error:
        return None

    finally:
        if conn is not None:
            conn.close()
