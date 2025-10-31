import pandas as pd
from core.models import (
    Institute,
    Student,
    Teacher,
    Program,
    Course,
    Enrollment,
    Result,
    Degree,
)
from django.db import transaction


# ---------------------
# Helper functions
# ---------------------
def load_dataframe(file_path):
    """Load CSV or Excel into a pandas DataFrame."""
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    return df.fillna("")


def get_institute_by_acronym(acronym, user):
    """Retrieve an institute object by its acronym for the current user's institution."""
    try:
        return Institute.objects.get(
            acronym=acronym.strip(), institution=user.institution
        )
    except Institute.DoesNotExist:
        return None


# ---------------------
# Ingestion functions
# ---------------------
@transaction.atomic
def ingest_students(file_path):
    df = load_dataframe(file_path)
    created, updated = 0, 0

    for _, row in df.iterrows():
        sid = str(row["student_id"]).strip()
        defaults = {
            "first_name": row["first_name"].strip(),
            "last_name": row["last_name"].strip(),
            "gender": str(row["gender (M/F)"]).upper().strip(),
            "birthdate": row["birthdate (YYYY-MM-DD)"],
        }
        obj, created_flag = Student.objects.update_or_create(
            student_id=sid, defaults=defaults
        )
        if created_flag:
            created += 1
        else:
            updated += 1
    return f"Students imported successfully: {created} created, {updated} updated."


@transaction.atomic
def ingest_teachers(file_path, user):
    df = load_dataframe(file_path)
    created, skipped, updated = 0, 0, 0

    for _, row in df.iterrows():
        acronym = str(row["institute_acronym"]).strip()
        teacher_id = str(row["teacher_id"]).strip()

        institute = get_institute_by_acronym(acronym, user)
        if not institute:
            skipped += 1
            continue

        defaults = {
            "first_name": row["first_name"].strip(),
            "last_name": row["last_name"].strip(),
            "grade": row["grade"].strip(),
            "status": row["status"].strip(),
            "institute": institute,
        }
        teacher, created_flag = Teacher.objects.update_or_create(
            teacher_id=teacher_id, defaults=defaults
        )
        if created_flag:
            created += 1
        else:
            updated += 1
    return f"Teachers imported successfully: {created} created, {updated} updated, {skipped} skipped."


@transaction.atomic
def ingest_programs(file_path, user):
    df = load_dataframe(file_path)
    created, skipped, updated = 0, 0, 0

    for _, row in df.iterrows():
        acronym = str(row["institute_acronym"]).strip()
        program_id = row["program_id"].strip()

        institute = get_institute_by_acronym(acronym, user)
        if not institute:
            skipped += 1
            continue

        defaults = {
            "name": row["name"].strip(),
            "domain": row["domain"].strip(),
            "level": row["level"].strip(),
            "institute": institute,
        }
        program, created_flag = Program.objects.update_or_create(
            program_id=program_id, defaults=defaults
        )
        if created_flag:
            created += 1
        else:
            updated += 1
    return f"Programs imported successfully: {created} created, {updated} updated, {skipped} skipped."


@transaction.atomic
def ingest_courses(file_path):
    df = load_dataframe(file_path)
    created, skipped, updated = 0, 0, 0

    for _, row in df.iterrows():
        try:
            program = Program.objects.get(program_id=row["program_id"].strip())
        except Program.DoesNotExist:
            skipped += 1
            continue

        teacher_id = str(row["teacher_id (optional)"]).strip()
        teacher = None
        if teacher_id:
            try:
                teacher = Teacher.objects.get(teacher_id=teacher_id)
            except Teacher.DoesNotExist:
                pass

        defaults = {
            "name": row["name"].strip(),
            "code": row["code"].strip(),
            "credits": int(row["credits"]),
            "semester": row["semester"].strip(),
            "program": program,
            "teacher": teacher,
        }
        course, created_flag = Course.objects.update_or_create(
            course_id=row["course_id"].strip(), defaults=defaults
        )
        if created_flag:
            created += 1
        else:
            updated += 1
    return f"Courses imported successfully: {created} created, {updated} updated, {skipped} skipped (invalid program)."


@transaction.atomic
def ingest_enrollments(file_path, user):
    df = load_dataframe(file_path)
    created, skipped, updated = 0, 0, 0

    for _, row in df.iterrows():
        acronym = str(row["institute_acronym"]).strip()
        institute = get_institute_by_acronym(acronym, user)
        if not institute:
            skipped += 1
            continue

        try:
            student = Student.objects.get(student_id=row["student_id"].strip())
            program = Program.objects.get(program_id=row["program_id"].strip())
        except (Student.DoesNotExist, Program.DoesNotExist):
            skipped += 1
            continue

        defaults = {
            "student": student,
            "program": program,
            "institute": institute,
            "academic_year": row["academic_year"].strip(),
            "status": row["status"].strip(),
        }
        enrollment, created_flag = Enrollment.objects.update_or_create(
            enrollment_id=row["enrollment_id"].strip(), defaults=defaults
        )
        if created_flag:
            created += 1
        else:
            updated += 1
    return f"Enrollments imported successfully: {created} created, {updated} updated, {skipped} skipped."


@transaction.atomic
def ingest_results(file_path, user):
    df = load_dataframe(file_path)
    created, skipped = 0, 0

    for _, row in df.iterrows():
        acronym = str(row["institute_acronym"]).strip()
        institute = get_institute_by_acronym(acronym, user)
        if not institute:
            skipped += 1
            continue

        try:
            student = Student.objects.get(student_id=row["student_id"].strip())
            course = Course.objects.get(course_id=row["course_id"].strip())
            enrollment = Enrollment.objects.filter(
                student=student, institute=institute
            ).first()
        except (Student.DoesNotExist, Course.DoesNotExist):
            skipped += 1
            continue

        if not enrollment:
            skipped += 1
            continue

        defaults = {
            "enrollment": enrollment,
            "course": course,
            "academic_year": row["academic_year"].strip(),
            "session": row["session"].strip(),
            "note": float(row["note"]),
        }
        Result.objects.update_or_create(
            result_id=row["result_id"].strip(), defaults=defaults
        )
        created += 1
    return f"Results imported successfully: {created} created, {skipped} skipped."


@transaction.atomic
def ingest_degrees(file_path, user):
    df = load_dataframe(file_path)
    created, skipped = 0, 0

    for _, row in df.iterrows():
        acronym = str(row["institute_acronym"]).strip()
        institute = get_institute_by_acronym(acronym, user)
        if not institute:
            skipped += 1
            continue

        try:
            student = Student.objects.get(student_id=row["student_id"].strip())
            enrollment = Enrollment.objects.filter(
                student=student, institute=institute
            ).first()
        except Student.DoesNotExist:
            skipped += 1
            continue

        if not enrollment:
            skipped += 1
            continue

        defaults = {
            "enrollment": enrollment,
            "date_awarded": row["date_awarded (YYYY-MM-DD)"],
            "degree_type": row["degree_type"].strip(),
            "name": row["name"].strip(),
        }
        Degree.objects.update_or_create(
            degree_id=row["degree_id"].strip(), defaults=defaults
        )
        created += 1
    return f"Degrees imported successfully: {created} created, {skipped} skipped."
