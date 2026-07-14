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


def initialize_conn():
    conn = sqlite3.connect("job_tracker.db")
    return conn


def initialize_cur(conn):
    return conn.cursor()


def add_application(application):
    conn = initialize_conn()

    cur = initialize_cur(conn)

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


def get_active_applications(sort_choice):
    conn = initialize_conn()
    conn.row_factory = sqlite3.Row

    cur = initialize_cur(conn)


    sort_options = {
        "Newest": 'application_date DESC',
        "Oldest": 'application_date ASC',
        "Company Name": 'company_name ASC',
        "Application Status": 'status ASC'
    }

    order_by = sort_options[sort_choice]

    cur.execute(f"""SELECT * 
                FROM applications 
                WHERE archived = 0
                ORDER BY {order_by}"""
            )
    applications = cur.fetchall()

    conn.close()

    return applications


def update_status(application_id, new_status):
    conn = initialize_conn()

    cur = initialize_cur(conn)

    cur.execute(
        """UPDATE applications
            SET status = ?
            WHERE id = ?""",
            (new_status, application_id)
    )

    conn.commit()
    conn.close()


def archived_status(application_id):
    conn = initialize_conn()

    cur = initialize_cur(conn)

    cur.execute(
        """UPDATE applications
            SET archived = 1
            WHERE id = ?""",
            (application_id,)
    )

    conn.commit()
    conn.close()


def edit_application_values(application_id, selected_column, updated_application_value):
    conn = initialize_conn()
    
    cur = initialize_cur(conn)
    
    trusted_columns = [
        'company_name',
        'job_title',
        'salary_range',
        'location',
        'notes'        
    ]
    if selected_column not in trusted_columns:
        return False
    
    cur.execute(f"""UPDATE applications
                SET {selected_column} = ?
                WHERE id = ?""",
                (updated_application_value, application_id)
                )
    conn.close()
    return True

def get_archived(sort_choice):
    conn = initialize_conn()
    conn.row_factory = sqlite3.Row

    cur = initialize_cur(conn)

    sort_options = {
        "Newest": 'application_date DESC',
        "Oldest": 'application_date ASC',
        "Company Name": 'company_name ASC',
        "Application Status": 'status ASC'
    }

    order_by = sort_options[sort_choice]

    cur.execute(f"""SELECT * 
                FROM applications 
                WHERE archived = 1
                ORDER BY {order_by}"""
            )
    applications = cur.fetchall()

    conn.close()
    return applications


def change_archive_status(application_id):
    conn = initialize_conn()

    cur = initialize_cur(conn)

    cur.execute(
        """UPDATE applications
            SET archived = 0
            WHERE id = ?""",
            (application_id,)
    )

    conn.commit()
    conn.close()


def return_filtered_apps(status, sort_choice):
    conn = initialize_conn()
    conn.row_factory = sqlite3.Row

    cur = initialize_cur(conn)

    sort_options = {
        "Newest": 'application_date DESC',
        "Oldest": 'application_date ASC',
        "Company Name": 'company_name ASC',
        "Application Status": 'status ASC'
    }

    order_by = sort_options[sort_choice]

    cur.execute(f"""SELECT * 
                FROM applications 
                WHERE archived = 0 
                AND 
                status = ?
                ORDER BY {order_by}""",
                (status,)
    )
    filtered_apps = cur.fetchall()

    conn.close()
    return filtered_apps


def get_search_results(keyword, sort_choice):
    conn = initialize_conn()
    conn.row_factory = sqlite3.Row

    cur = initialize_cur(conn)

    sort_options = {
        "Newest": 'application_date DESC',
        "Oldest": 'application_date ASC',
        "Company Name": 'company_name ASC',
        "Application Status": 'status ASC'
    }

    order_by = sort_options[sort_choice]

    search_pattern = f"%{keyword}%"

    cur.execute(f"""SELECT * 
                FROM applications
                WHERE archived = 0 
                AND (
                company_name LIKE ?
                OR job_title LIKE ?
                OR salary_range LIKE ?
                OR location LIKE ?
                OR notes LIKE ?)
                ORDER BY {order_by}""",
                (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern)
    )
    search_results = cur.fetchall()

    conn.close()
    return search_results