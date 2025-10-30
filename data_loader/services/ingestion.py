import pandas as pd
from core.models import (
    Student,
    Program,
    Course,
    Institution,
    Enrollment,
    Result,
    AcademicYear,
)


def _read_file(file_path):
    if file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        return pd.read_excel(file_path)
    return pd.read_csv(file_path)


# --------- STUDENTS ----------
def ingest_students(file_path):
    df = _read_file(file_path)
    for _, row in df.iterrows():
        institution = Institution.objects.get(code=row["institution_code"])
        Student.objects.update_or_create(
            student_id=row["student_id"],
            defaults={
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "gender": row["gender"],
                "birth_date": row["birth_date"],
                "institution": institution,
            },
        )


# --------- PROGRAMS ----------
def ingest_programs(file_path):
    df = _read_file(file_path)
    for _, row in df.iterrows():
        institution = Institution.objects.get(code=row["institution_code"])
        Program.objects.update_or_create(
            name=row["program_name"], institution=institution
        )


# --------- COURSES ----------
def ingest_courses(file_path):
    df = _read_file(file_path)
    for _, row in df.iterrows():
        institution = Institution.objects.get(code=row["institution_code"])
        program = Program.objects.get(name=row["program_name"], institution=institution)
        Course.objects.update_or_create(
            code=row["course_code"],
            defaults={
                "name": row["course_name"],
                "program": program,
                "credits": row["credits"],
            },
        )


# --------- ENROLLMENTS ----------
def ingest_enrollments(file_path):
    df = _read_file(file_path)
    for _, row in df.iterrows():
        student = Student.objects.get(student_id=row["student_id"])
        program = Program.objects.get(name=row["program_name"])
        year = AcademicYear.objects.get(name=row["academic_year"])
        Enrollment.objects.update_or_create(
            student=student, program=program, academic_year=year
        )


# --------- RESULTS ----------
def ingest_results(file_path):
    df = _read_file(file_path)
    for _, row in df.iterrows():
        student = Student.objects.get(student_id=row["student_id"])
        course = Course.objects.get(code=row["course_code"])
        year = AcademicYear.objects.get(name=row["academic_year"])
        Result.objects.update_or_create(
            student=student,
            course=course,
            academic_year=year,
            defaults={"grade": row["grade"]},
        )
