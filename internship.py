import sqlite3

from database import get_connection


def add_internship(
    company_id,
    title,
    description,
    skills_required,
    duration_months,
    stipend,
    location,
    mode,
    openings,
    deadline,
    status
):
    connection = get_connection()

    connection.execute("""
        INSERT INTO Internships
        (
            company_id,
            title,
            description,
            skills_required,
            duration_months,
            stipend,
            location,
            mode,
            openings,
            deadline,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        company_id,
        title,
        description,
        skills_required,
        duration_months,
        stipend,
        location,
        mode,
        openings,
        deadline,
        status
    ))

    connection.commit()
    connection.close()


def get_all_internships():
    connection = get_connection()

    internships = connection.execute("""
        SELECT
            Internships.internship_id,
            Companies.company_name,
            Internships.title,
            Internships.description,
            Internships.skills_required,
            Internships.duration_months,
            Internships.stipend,
            Internships.location,
            Internships.mode,
            Internships.openings,
            Internships.deadline,
            Internships.status
        FROM Internships
        JOIN Companies
        ON Internships.company_id = Companies.company_id
        ORDER BY Internships.internship_id DESC
    """).fetchall()

    connection.close()

    return internships


def search_internships(search_text):
    connection = get_connection()

    internships = connection.execute("""
        SELECT
            Internships.internship_id,
            Companies.company_name,
            Internships.title,
            Internships.description,
            Internships.skills_required,
            Internships.duration_months,
            Internships.stipend,
            Internships.location,
            Internships.mode,
            Internships.openings,
            Internships.deadline,
            Internships.status
        FROM Internships
        JOIN Companies
        ON Internships.company_id = Companies.company_id
        WHERE
            CAST(Internships.internship_id AS TEXT) LIKE ?
            OR Companies.company_name LIKE ?
            OR Internships.title LIKE ?
            OR Internships.description LIKE ?
            OR Internships.skills_required LIKE ?
            OR CAST(Internships.duration_months AS TEXT) LIKE ?
            OR CAST(Internships.stipend AS TEXT) LIKE ?
            OR Internships.location LIKE ?
            OR Internships.mode LIKE ?
            OR Internships.status LIKE ?
        ORDER BY Internships.internship_id DESC
    """, (
        f"%{search_text}%",
        f"%{search_text}%",
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

    return internships


def delete_internship(internship_id):
    connection = get_connection()

    try:
        connection.execute("""
            DELETE FROM Internships
            WHERE internship_id = ?
        """, (internship_id,))

        connection.commit()

    except sqlite3.IntegrityError:
        connection.rollback()
        raise ValueError(
            "This internship cannot be deleted because it has existing applications."
        )

    finally:
        connection.close()