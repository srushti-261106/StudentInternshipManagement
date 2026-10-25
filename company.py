import sqlite3

from database import get_connection


def add_company(company_name, industry, location, email, website):
    connection = get_connection()

    connection.execute("""
        INSERT INTO Companies
        (company_name, industry, location, email, website)
        VALUES (?, ?, ?, ?, ?)
    """, (
        company_name,
        industry,
        location,
        email,
        website
    ))

    connection.commit()
    connection.close()


def get_all_companies():
    connection = get_connection()

    companies = connection.execute("""
        SELECT *
        FROM Companies
        ORDER BY company_id DESC
    """).fetchall()

    connection.close()

    return companies


def search_companies(search_text):
    connection = get_connection()

    companies = connection.execute("""
        SELECT *
        FROM Companies
        WHERE
            CAST(company_id AS TEXT) LIKE ?
            OR company_name LIKE ?
            OR industry LIKE ?
            OR location LIKE ?
            OR email LIKE ?
            OR website LIKE ?
        ORDER BY company_id DESC
    """, (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%"
    )).fetchall()

    connection.close()

    return companies


def delete_company(company_id):
    connection = get_connection()

    try:
        connection.execute("""
            DELETE FROM Companies
            WHERE company_id = ?
        """, (company_id,))

        connection.commit()

    except sqlite3.IntegrityError:
        connection.rollback()
        raise ValueError(
            "This company cannot be deleted because it has existing internships."
        )

    finally:
        connection.close()