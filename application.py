import sqlite3

from database import get_connection


def add_application(
    student_id,
    internship_id,
    application_date,
    status="Applied",
    interview_date=None,
    remarks=None
):
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO Applications
            (
                student_id,
                internship_id,
                application_date,
                status,
                interview_date,
                remarks
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            internship_id,
            application_date,
            status,
            interview_date,
            remarks
        ))

        connection.commit()

    except sqlite3.IntegrityError:
        connection.rollback()
        raise ValueError(
            "This student has already applied for this internship."
        )

    finally:
        connection.close()


def get_all_applications():
    connection = get_connection()

    applications = connection.execute("""
        SELECT
            Applications.application_id,
            Students.student_id,
            Students.name,
            Companies.company_name,
            Internships.internship_id,
            Internships.title,
            Applications.application_date,
            Applications.status,
            Applications.interview_date,
            Applications.remarks
        FROM Applications
        JOIN Students
            ON Applications.student_id = Students.student_id
        JOIN Internships
            ON Applications.internship_id = Internships.internship_id
        JOIN Companies
            ON Internships.company_id = Companies.company_id
        ORDER BY Applications.application_id DESC
    """).fetchall()

    connection.close()

    return applications


def search_applications(search_text):
    connection = get_connection()

    applications = connection.execute("""
        SELECT
            Applications.application_id,
            Students.student_id,
            Students.name,
            Companies.company_name,
            Internships.internship_id,
            Internships.title,
            Applications.application_date,
            Applications.status,
            Applications.interview_date,
            Applications.remarks
        FROM Applications
        JOIN Students
            ON Applications.student_id = Students.student_id
        JOIN Internships
            ON Applications.internship_id = Internships.internship_id
        JOIN Companies
            ON Internships.company_id = Companies.company_id
        WHERE
            CAST(Applications.application_id AS TEXT) LIKE ?
            OR Students.name LIKE ?
            OR Companies.company_name LIKE ?
            OR Internships.title LIKE ?
            OR Applications.status LIKE ?
            OR Applications.remarks LIKE ?
        ORDER BY Applications.application_id DESC
    """, (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%"
    )).fetchall()

    connection.close()

    return applications


def update_application_status(application_id, status):
    connection = get_connection()

    connection.execute("""
        UPDATE Applications
        SET status = ?
        WHERE application_id = ?
    """, (
        status,
        application_id
    ))

    connection.commit()
    connection.close()


def delete_application(application_id):
    connection = get_connection()

    connection.execute("""
        DELETE FROM Applications
        WHERE application_id = ?
    """, (application_id,))

    connection.commit()
    connection.close()