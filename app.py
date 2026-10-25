import streamlit as st

from database import (
    create_students_table,
    create_companies_table,
    create_internships_table,
    create_applications_table,
    create_indexes,
    get_dashboard_statistics,
    get_internship_report,
    get_application_status_summary,
    get_company_application_summary,
    get_student_application_summary,
    get_selected_students
)

from student import (
    add_student,
    get_all_students,
    search_students,
    delete_student
)

from company import (
    add_company,
    get_all_companies,
    search_companies,
    delete_company
)

from internship import (
    add_internship,
    get_all_internships,
    search_internships,
    delete_internship
)

from application import (
    add_application,
    get_all_applications,
    search_applications,
    update_application_status,
    delete_application
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

create_students_table()
create_companies_table()
create_internships_table()
create_applications_table()
create_indexes()


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Student Internship Management System",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# MAIN TITLE
# ============================================================

st.title("🎓 Student Internship Management System")


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("Navigation")

menu = st.sidebar.selectbox(
    "Select a module",
    [
        "Dashboard",
        "Students",
        "Companies",
        "Internships",
        "Applications"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    st.write(
        "Overview of the Student Internship Management System"
    )

    (
        student_count,
        company_count,
        internship_count,
        application_count,
        open_internship_count,
        selected_count
    ) = get_dashboard_statistics()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            student_count
        )

    with col2:
        st.metric(
            "🏢 Total Companies",
            company_count
        )

    with col3:
        st.metric(
            "💼 Total Internships",
            internship_count
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "📋 Total Applications",
            application_count
        )

    with col5:
        st.metric(
            "🟢 Open Internships",
            open_internship_count
        )

    with col6:
        st.metric(
            "🎯 Selected Students",
            selected_count
        )

    st.divider()

    st.subheader("System Overview")

    st.info(
        "This system manages students, companies, internships "
        "and internship applications using a relational database."
    )

    st.divider()

    # ========================================================
    # DBMS REPORTS
    # ========================================================

    st.header("📈 DBMS Reports")

    report = st.selectbox(
        "Select a report",
        [
            "Internship & Company Report",
            "Application Status Summary",
            "Company-wise Application Summary",
            "Student Application Summary",
            "Selected Students"
        ]
    )

    if report == "Internship & Company Report":

        st.subheader(
            "💼 Internship & Company Report"
        )

        internship_report = get_internship_report()

        if internship_report:

            for row in internship_report:

                st.write(
                    f"**{row[0]}** — {row[1]}"
                )

                st.write(
                    f"Industry: {row[2]} | "
                    f"Location: {row[3]} | "
                    f"Mode: {row[4]}"
                )

                st.write(
                    f"Duration: {row[5]} months | "
                    f"Stipend: ₹{row[6]:,.0f} | "
                    f"Openings: {row[7]} | "
                    f"Status: {row[8]}"
                )

                st.divider()

        else:

            st.info(
                "No internship data available."
            )

    elif report == "Application Status Summary":

        st.subheader(
            "📋 Application Status Summary"
        )

        status_summary = (
            get_application_status_summary()
        )

        if status_summary:

            for row in status_summary:

                st.metric(
                    row[0],
                    row[1]
                )

        else:

            st.info(
                "No application data available."
            )

    elif report == "Company-wise Application Summary":

        st.subheader(
            "🏢 Company-wise Application Summary"
        )

        company_summary = (
            get_company_application_summary()
        )

        if company_summary:

            for row in company_summary:

                st.write(
                    f"**{row[0]}**"
                )

                st.write(
                    f"Total Applications: {row[1]}"
                )

                st.divider()

        else:

            st.info(
                "No company data available."
            )

    elif report == "Student Application Summary":

        st.subheader(
            "👨‍🎓 Student Application Summary"
        )

        student_summary = (
            get_student_application_summary()
        )

        if student_summary:

            for row in student_summary:

                st.write(
                    f"**{row[0]}**"
                )

                st.write(
                    f"Department: {row[1]} | "
                    f"CGPA: {row[2]} | "
                    f"Applications: {row[3]}"
                )

                st.divider()

        else:

            st.info(
                "No student data available."
            )

    elif report == "Selected Students":

        st.subheader(
            "🎯 Selected Students"
        )

        selected_students = (
            get_selected_students()
        )

        if selected_students:

            for row in selected_students:

                st.write(
                    f"**{row[0]}**"
                )

                st.write(
                    f"Department: {row[1]} | "
                    f"CGPA: {row[2]}"
                )

                st.write(
                    f"Company: {row[3]} | "
                    f"Internship: {row[4]}"
                )

                st.write(
                    f"Application Date: {row[5]}"
                )

                st.divider()

        else:

            st.info(
                "No selected students yet."
            )


# ============================================================
# STUDENTS
# ============================================================

elif menu == "Students":

    st.header("👨‍🎓 Student Management")

    st.subheader("Add New Student")

    with st.form("student_form"):

        name = st.text_input("Student Name")

        email = st.text_input("Email")

        phone = st.text_input("Phone Number")

        department = st.text_input("Department")

        year = st.number_input(
            "Year",
            min_value=1,
            max_value=6,
            step=1
        )

        cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=10.0,
            step=0.1
        )

        skills = st.text_input("Skills")

        submitted = st.form_submit_button(
            "Add Student"
        )

        if submitted:

            if (
                not name
                or not email
                or not phone
                or not department
            ):

                st.error(
                    "Please fill in all required fields."
                )

            else:

                try:

                    add_student(
                        name,
                        email,
                        phone,
                        department,
                        year,
                        cgpa,
                        skills
                    )

                    st.success(
                        "Student added successfully!"
                    )

                except Exception as error:

                    st.error(
                        f"Error: {error}"
                    )

    st.divider()

    st.subheader("🔍 Search Student")

    search_text = st.text_input(
        "Search by Student ID, Name, Email, Phone, Department, Year, CGPA or Skills",
        placeholder="Enter search text..."
    )

    if search_text:

        students = search_students(
            search_text
        )

    else:

        students = get_all_students()

    st.subheader("Student Information")

    if students:

        for student in students:

            with st.container(border=True):

                st.write(
                    f"### 👤 {student[1]}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Student ID:** {student[0]}"
                    )

                    st.write(
                        f"**Email:** {student[2]}"
                    )

                    st.write(
                        f"**Phone:** {student[3]}"
                    )

                    st.write(
                        f"**Department:** {student[4]}"
                    )

                with col2:

                    st.write(
                        f"**Year:** {student[5]}"
                    )

                    st.write(
                        f"**CGPA:** {student[6]}"
                    )

                    st.write(
                        f"**Skills:** {student[7]}"
                    )

    else:

        st.warning(
            "No student found."
        )

    st.divider()

    st.subheader("🗑️ Delete Student")

    all_students_for_delete = (
        get_all_students()
    )

    if all_students_for_delete:

        student_delete_options = {
            f"{student[1]} (ID: {student[0]})":
                student[0]
            for student in all_students_for_delete
        }

        selected_student_delete = st.selectbox(
            "Select Student to Delete",
            list(student_delete_options.keys())
        )

        if st.button(
            "Delete Student",
            type="secondary"
        ):

            student_id = student_delete_options[
                selected_student_delete
            ]

            try:

                delete_student(
                    student_id
                )

                st.success(
                    "Student deleted successfully!"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Error: {error}"
                )

    else:

        st.info(
            "There are no students to delete."
        )


# ============================================================
# COMPANIES
# ============================================================

elif menu == "Companies":

    st.header("🏢 Company Management")

    st.subheader("Add New Company")

    with st.form("company_form"):

        company_name = st.text_input(
            "Company Name"
        )

        industry = st.text_input(
            "Industry"
        )

        location = st.text_input(
            "Location"
        )

        email = st.text_input(
            "Company Email"
        )

        website = st.text_input(
            "Website"
        )

        submitted = st.form_submit_button(
            "Add Company"
        )

        if submitted:

            if not company_name:

                st.error(
                    "Company name is required."
                )

            else:

                try:

                    add_company(
                        company_name,
                        industry,
                        location,
                        email,
                        website
                    )

                    st.success(
                        "Company added successfully!"
                    )

                except Exception as error:

                    st.error(
                        f"Error: {error}"
                    )

    st.divider()

    st.subheader("🔍 Search Company")

    search_text = st.text_input(
        "Search by Company ID, Name, Industry, Location, Email or Website",
        placeholder="Enter search text..."
    )

    if search_text:

        companies = search_companies(
            search_text
        )

    else:

        companies = get_all_companies()

    st.subheader("Company Information")

    if companies:

        for company in companies:

            with st.container(border=True):

                st.write(
                    f"### 🏢 {company[1]}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Company ID:** {company[0]}"
                    )

                    st.write(
                        f"**Industry:** {company[2]}"
                    )

                    st.write(
                        f"**Location:** {company[3]}"
                    )

                with col2:

                    st.write(
                        f"**Email:** {company[4]}"
                    )

                    st.write(
                        f"**Website:** {company[5]}"
                    )

    else:

        st.info(
            "No companies found."
        )

    st.divider()

    st.subheader("🗑️ Delete Company")

    all_companies_for_delete = (
        get_all_companies()
    )

    if all_companies_for_delete:

        company_delete_options = {
            f"{company[1]} (ID: {company[0]})":
                company[0]
            for company in all_companies_for_delete
        }

        selected_company_delete = st.selectbox(
            "Select Company to Delete",
            list(company_delete_options.keys())
        )

        if st.button(
            "Delete Company",
            type="secondary"
        ):

            company_id = company_delete_options[
                selected_company_delete
            ]

            try:

                delete_company(
                    company_id
                )

                st.success(
                    "Company deleted successfully!"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Error: {error}"
                )

    else:

        st.info(
            "There are no companies to delete."
        )


# ============================================================
# INTERNSHIPS
# ============================================================

elif menu == "Internships":

    st.header("💼 Internship Management")

    st.subheader("Add New Internship")

    companies = get_all_companies()

    if not companies:

        st.warning(
            "Please add at least one company before creating an internship."
        )

    else:

        company_options = {
            f"{company[1]} (ID: {company[0]})":
                company[0]
            for company in companies
        }

        with st.form("internship_form"):

            selected_company = st.selectbox(
                "Company",
                list(company_options.keys())
            )

            title = st.text_input(
                "Internship Title"
            )

            description = st.text_area(
                "Description"
            )

            skills_required = st.text_input(
                "Skills Required"
            )

            duration_months = st.number_input(
                "Duration (Months)",
                min_value=1,
                max_value=24,
                value=3,
                step=1
            )

            stipend = st.number_input(
                "Stipend (₹ per month)",
                min_value=0.0,
                step=1000.0
            )

            location = st.text_input(
                "Location"
            )

            mode = st.selectbox(
                "Work Mode",
                [
                    "On-site",
                    "Hybrid",
                    "Remote"
                ]
            )

            openings = st.number_input(
                "Number of Openings",
                min_value=1,
                max_value=100,
                value=1,
                step=1
            )

            deadline = st.date_input(
                "Application Deadline"
            )

            status = st.selectbox(
                "Status",
                [
                    "Open",
                    "Closed"
                ]
            )

            submitted = st.form_submit_button(
                "Add Internship"
            )

            if submitted:

                if not title:

                    st.error(
                        "Internship title is required."
                    )

                else:

                    try:

                        company_id = company_options[
                            selected_company
                        ]

                        add_internship(
                            company_id,
                            title,
                            description,
                            skills_required,
                            duration_months,
                            stipend,
                            location,
                            mode,
                            openings,
                            str(deadline),
                            status
                        )

                        st.success(
                            "Internship added successfully!"
                        )

                    except Exception as error:

                        st.error(
                            f"Error: {error}"
                        )

    st.divider()

    st.subheader("🔍 Search Internship")

    search_text = st.text_input(
        "Search by Internship ID, Company, Title, Skills, Location, Mode or Status",
        placeholder="Enter search text..."
    )

    if search_text:

        internships = search_internships(
            search_text
        )

    else:

        internships = get_all_internships()

    st.subheader("Internship Information")

    if internships:

        for internship in internships:

            with st.container(border=True):

                st.write(
                    f"### 💼 {internship[2]}"
                )

                st.write(
                    f"**Company:** {internship[1]}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Internship ID:** {internship[0]}"
                    )

                    st.write(
                        f"**Skills Required:** {internship[4]}"
                    )

                    st.write(
                        f"**Duration:** {internship[5]} months"
                    )

                    st.write(
                        f"**Stipend:** ₹{internship[6]:,.0f}"
                    )

                    st.write(
                        f"**Location:** {internship[7]}"
                    )

                with col2:

                    st.write(
                        f"**Mode:** {internship[8]}"
                    )

                    st.write(
                        f"**Openings:** {internship[9]}"
                    )

                    st.write(
                        f"**Deadline:** {internship[10]}"
                    )

                    st.write(
                        f"**Status:** {internship[11]}"
                    )

                st.write(
                    f"**Description:** {internship[3]}"
                )

    else:

        st.info(
            "No internships found."
        )

    st.divider()

    st.subheader("🗑️ Delete Internship")

    all_internships_for_delete = (
        get_all_internships()
    )

    if all_internships_for_delete:

        internship_delete_options = {
            f"{internship[2]} - {internship[1]} "
            f"(ID: {internship[0]})":
                internship[0]
            for internship in all_internships_for_delete
        }

        selected_internship_delete = st.selectbox(
            "Select Internship to Delete",
            list(
                internship_delete_options.keys()
            )
        )

        if st.button(
            "Delete Internship",
            type="secondary"
        ):

            internship_id = internship_delete_options[
                selected_internship_delete
            ]

            try:

                delete_internship(
                    internship_id
                )

                st.success(
                    "Internship deleted successfully!"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Error: {error}"
                )

    else:

        st.info(
            "There are no internships to delete."
        )


# ============================================================
# APPLICATIONS
# ============================================================

elif menu == "Applications":

    st.header("📋 Application Management")

    st.subheader("Apply for an Internship")

    students = get_all_students()

    internships = get_all_internships()

    if not students:

        st.warning(
            "Please add at least one student before creating an application."
        )

    elif not internships:

        st.warning(
            "Please add at least one internship before creating an application."
        )

    else:

        student_options = {
            f"{student[1]} (ID: {student[0]})":
                student[0]
            for student in students
        }

        internship_options = {
            f"{internship[2]} - {internship[1]} "
            f"(ID: {internship[0]})":
                internship[0]
            for internship in internships
        }

        with st.form("application_form"):

            selected_student = st.selectbox(
                "Student",
                list(student_options.keys())
            )

            selected_internship = st.selectbox(
                "Internship",
                list(internship_options.keys())
            )

            application_date = st.date_input(
                "Application Date"
            )

            status = st.selectbox(
                "Application Status",
                [
                    "Applied",
                    "Shortlisted",
                    "Interview",
                    "Selected",
                    "Rejected"
                ]
            )

            interview_date = st.date_input(
                "Interview Date",
                value=None
            )

            remarks = st.text_area(
                "Remarks"
            )

            submitted = st.form_submit_button(
                "Submit Application"
            )

            if submitted:

                try:

                    student_id = student_options[
                        selected_student
                    ]

                    internship_id = internship_options[
                        selected_internship
                    ]

                    interview_date_value = (
                        str(interview_date)
                        if interview_date
                        else None
                    )

                    add_application(
                        student_id,
                        internship_id,
                        str(application_date),
                        status,
                        interview_date_value,
                        remarks
                    )

                    st.success(
                        "Application submitted successfully!"
                    )

                except Exception as error:

                    st.error(
                        f"Error: {error}"
                    )

    st.divider()

    st.subheader("🔄 Update Application Status")

    applications = get_all_applications()

    if applications:

        application_options = {
            f"Application {application[0]} - "
            f"{application[2]} - "
            f"{application[5]}":
                application[0]
            for application in applications
        }

        selected_application = st.selectbox(
            "Select Application",
            list(application_options.keys())
        )

        new_status = st.selectbox(
            "New Status",
            [
                "Applied",
                "Shortlisted",
                "Interview",
                "Selected",
                "Rejected"
            ],
            key="new_application_status"
        )

        if st.button(
            "Update Status"
        ):

            application_id = application_options[
                selected_application
            ]

            update_application_status(
                application_id,
                new_status
            )

            st.success(
                "Application status updated successfully!"
            )

            st.rerun()

    st.divider()

    st.subheader("🗑️ Delete Application")

    all_applications_for_delete = (
        get_all_applications()
    )

    if all_applications_for_delete:

        application_delete_options = {
            f"Application {application[0]} - "
            f"{application[2]} - "
            f"{application[5]}":
                application[0]
            for application in all_applications_for_delete
        }

        selected_application_delete = st.selectbox(
            "Select Application to Delete",
            list(
                application_delete_options.keys()
            )
        )

        if st.button(
            "Delete Application",
            type="secondary"
        ):

            application_id = (
                application_delete_options[
                    selected_application_delete
                ]
            )

            try:

                delete_application(
                    application_id
                )

                st.success(
                    "Application deleted successfully!"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Error: {error}"
                )

    else:

        st.info(
            "There are no applications to delete."
        )

    st.divider()

    st.subheader("🔍 Search Applications")

    search_text = st.text_input(
        "Search by Application ID, Student Name, Company, Internship, Status or Remarks",
        placeholder="Enter search text..."
    )

    if search_text:

        applications = search_applications(
            search_text
        )

    else:

        applications = get_all_applications()

    st.subheader("Application Information")

    if applications:

        for application in applications:

            with st.container(border=True):

                st.write(
                    f"### 📋 Application ID: {application[0]}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Student:** {application[2]}"
                    )

                    st.write(
                        f"**Student ID:** {application[1]}"
                    )

                    st.write(
                        f"**Company:** {application[3]}"
                    )

                    st.write(
                        f"**Internship:** {application[5]}"
                    )

                    st.write(
                        f"**Internship ID:** {application[4]}"
                    )

                with col2:

                    st.write(
                        f"**Application Date:** {application[6]}"
                    )

                    st.write(
                        f"**Status:** {application[7]}"
                    )

                    st.write(
                        f"**Interview Date:** {application[8]}"
                    )

                    st.write(
                        f"**Remarks:** {application[9]}"
                    )

    else:

        st.info(
            "No applications found."
        )