# Student Internship Management System

A database management system project built using **Python, Streamlit, and SQLite** to manage student information, companies, internship opportunities, and internship applications.

## About the Project

The Student Internship Management System provides a centralized platform to organize internship-related information. It helps manage student records, company details, internship listings, and application statuses.

## Features

* **Student Management:** Store and manage student details.
* **Company Management:** Maintain company information.
* **Internship Management:** Create, view, update, and manage internship listings.
* **Application Management:** Track student applications and their statuses.
* **Search and Filter:** Find relevant records easily.
* **Dashboard:** View summary statistics for students, companies, internships, and applications.
* **Reports:** View internship-related information for analysis.

## Technologies Used

* Python
* Streamlit
* SQLite
* SQL
* Visual Studio Code
* Git and GitHub

## Project Structure

```text
StudentInternshipManagement/
├── app.py
├── database.py
├── student.py
├── company.py
├── internship.py
├── application.py
├── requirements.txt
├── README.md
└── internship.db
```

*Note: The database file is excluded from this public repository.*

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/srushti-261106/StudentInternshipManagement.git
```

### 2. Navigate to the Project Folder

```bash
cd StudentInternshipManagement
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application should open in your browser.

**Note:** The SQLite database file is not included in this repository. The application may require database initialization or setup before it can run successfully on another computer.

## Database Modules

The system manages four main entities:

1. **Students** — student information and skills.
2. **Companies** — company details.
3. **Internships** — available internship opportunities.
4. **Applications** — student applications and their statuses.

The database connects companies to internships and connects students to internships through application records.

## Purpose

This project was developed as an academic DBMS project to demonstrate database design, SQL operations, CRUD functionality, record management, and a Python-based user interface.

## Author

**Srushti Patole**
