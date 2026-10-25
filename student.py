import sqlite3

from database import get_connection


def add_student(name, email, phone, department, year, cgpa, skills):
    connection = get_connection()

    connection.execute("""
        INSERT INTO Students
        (name, email, phone, department, year, cgpa, skills)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        department,
        year,
        cgpa,
        skills
    ))

    connection.commit()
    connection.close()


def get_all_students():
    connection = get_connection()

    students = connection.execute("""
        SELECT *
        FROM Students
        ORDER BY student_id DESC
    """).fetchall()

    connection.close()

    return students


def search_students(search_text):
    connection = get_connection()

    students = connection.execute("""
        SELECT *
        FROM Students
        WHERE
            CAST(student_id AS TEXT) LIKE ?
            OR name LIKE ?
            OR email LIKE ?
            OR phone LIKE ?
            OR department LIKE ?
            OR CAST(year AS TEXT) LIKE ?
            OR CAST(cgpa AS TEXT) LIKE ?
            OR skills LIKE ?
        ORDER BY student_id DESC
    """, (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%"
    )).fetchall()

    connection.close()

    return students


def delete_student(student_id):
    connection = get_connection()

    try:
        connection.execute("""
            DELETE FROM Students
            WHERE student_id = ?
        """, (student_id,))

        connection.commit()

    except sqlite3.IntegrityError:
        connection.rollback()
        raise ValueError(
            "This student cannot be deleted because they have existing applications."
        )

    finally:
        connection.close()