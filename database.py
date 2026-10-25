import sqlite3


def get_connection():
    connection = sqlite3.connect("internship.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# ============================================================
# CREATE STUDENTS TABLE
# ============================================================

def create_students_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            year INTEGER NOT NULL,
            cgpa REAL CHECK(cgpa >= 0 AND cgpa <= 10),
            skills TEXT
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# CREATE COMPANIES TABLE
# ============================================================

def create_companies_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS Companies (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT UNIQUE NOT NULL,
            industry TEXT,
            location TEXT,
            email TEXT,
            website TEXT
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# CREATE INTERNSHIPS TABLE
# ============================================================

def create_internships_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS Internships (
            internship_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            skills_required TEXT,
            duration_months INTEGER NOT NULL,
            stipend REAL DEFAULT 0,
            location TEXT,
            mode TEXT,
            openings INTEGER DEFAULT 1,
            deadline TEXT,
            status TEXT DEFAULT 'Open',
            FOREIGN KEY (company_id) REFERENCES Companies(company_id)
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# CREATE APPLICATIONS TABLE
# ============================================================

def create_applications_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS Applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            internship_id INTEGER NOT NULL,
            application_date TEXT NOT NULL,
            status TEXT DEFAULT 'Applied',
            interview_date TEXT,
            remarks TEXT,
            UNIQUE(student_id, internship_id),
            FOREIGN KEY (student_id) REFERENCES Students(student_id),
            FOREIGN KEY (internship_id) REFERENCES Internships(internship_id)
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# CREATE INDEXES
# ============================================================

def create_indexes():
    connection = get_connection()

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_students_name
        ON Students(name)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_students_department
        ON Students(department)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_companies_name
        ON Companies(company_name)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_companies_industry
        ON Companies(industry)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_internships_company
        ON Internships(company_id)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_internships_status
        ON Internships(status)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_applications_student
        ON Applications(student_id)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_applications_internship
        ON Applications(internship_id)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_applications_status
        ON Applications(status)
    """)

    connection.commit()
    connection.close()


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

def get_dashboard_statistics():

    connection = get_connection()

    student_count = connection.execute("""
        SELECT COUNT(*)
        FROM Students
    """).fetchone()[0]

    company_count = connection.execute("""
        SELECT COUNT(*)
        FROM Companies
    """).fetchone()[0]

    internship_count = connection.execute("""
        SELECT COUNT(*)
        FROM Internships
    """).fetchone()[0]

    application_count = connection.execute("""
        SELECT COUNT(*)
        FROM Applications
    """).fetchone()[0]

    open_internship_count = connection.execute("""
        SELECT COUNT(*)
        FROM Internships
        WHERE status = 'Open'
    """).fetchone()[0]

    selected_count = connection.execute("""
        SELECT COUNT(*)
        FROM Applications
        WHERE status = 'Selected'
    """).fetchone()[0]

    connection.close()

    return (
        student_count,
        company_count,
        internship_count,
        application_count,
        open_internship_count,
        selected_count
    )


# ============================================================
# DBMS REPORT 1
# INTERNSHIPS WITH COMPANY DETAILS
# ============================================================

def get_internship_report():

    connection = get_connection()

    report = connection.execute("""
        SELECT
            Internships.title,
            Companies.company_name,
            Companies.industry,
            Internships.location,
            Internships.mode,
            Internships.duration_months,
            Internships.stipend,
            Internships.openings,
            Internships.status
        FROM Internships
        INNER JOIN Companies
            ON Internships.company_id = Companies.company_id
        ORDER BY Internships.stipend DESC
    """).fetchall()

    connection.close()

    return report


# ============================================================
# DBMS REPORT 2
# APPLICATION STATUS SUMMARY
# ============================================================

def get_application_status_summary():

    connection = get_connection()

    summary = connection.execute("""
        SELECT
            status,
            COUNT(*) AS total_applications
        FROM Applications
        GROUP BY status
        ORDER BY total_applications DESC
    """).fetchall()

    connection.close()

    return summary


# ============================================================
# DBMS REPORT 3
# COMPANY-WISE APPLICATION COUNT
# ============================================================

def get_company_application_summary():

    connection = get_connection()

    summary = connection.execute("""
        SELECT
            Companies.company_name,
            COUNT(Applications.application_id) AS total_applications
        FROM Companies
        LEFT JOIN Internships
            ON Companies.company_id = Internships.company_id
        LEFT JOIN Applications
            ON Internships.internship_id = Applications.internship_id
        GROUP BY
            Companies.company_id,
            Companies.company_name
        ORDER BY total_applications DESC
    """).fetchall()

    connection.close()

    return summary


# ============================================================
# DBMS REPORT 4
# STUDENT APPLICATION SUMMARY
# ============================================================

def get_student_application_summary():

    connection = get_connection()

    summary = connection.execute("""
        SELECT
            Students.name,
            Students.department,
            Students.cgpa,
            COUNT(Applications.application_id) AS total_applications
        FROM Students
        LEFT JOIN Applications
            ON Students.student_id = Applications.student_id
        GROUP BY
            Students.student_id,
            Students.name,
            Students.department,
            Students.cgpa
        ORDER BY total_applications DESC
    """).fetchall()

    connection.close()

    return summary


# ============================================================
# DBMS REPORT 5
# SELECTED STUDENTS
# ============================================================

def get_selected_students():

    connection = get_connection()

    selected_students = connection.execute("""
        SELECT
            Students.name,
            Students.department,
            Students.cgpa,
            Companies.company_name,
            Internships.title,
            Applications.application_date
        FROM Applications
        INNER JOIN Students
            ON Applications.student_id = Students.student_id
        INNER JOIN Internships
            ON Applications.internship_id = Internships.internship_id
        INNER JOIN Companies
            ON Internships.company_id = Companies.company_id
        WHERE Applications.status = 'Selected'
        ORDER BY Students.cgpa DESC
    """).fetchall()

    connection.close()

    return selected_students