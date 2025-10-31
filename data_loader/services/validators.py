import pandas as pd
from core.models import Institute, Program, Course, Student, Teacher


# -------------
# Helper utils
# -------------
def load_dataframe(file_path):
    """Load CSV or Excel into a pandas DataFrame"""
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    return df.fillna("")  # éviter les NaN


def check_required_columns(df, required_cols):
    """Retourne la liste des colonnes manquantes"""
    return [col for col in required_cols if col not in df.columns]


# -------------
# Validators
# -------------


def validate_students_file(file_path):
    errors = []
    df = load_dataframe(file_path)
    required = [
        "student_id",
        "first_name",
        "last_name",
        "gender (M/F)",
        "birthdate (YYYY-MM-DD)",
    ]

    # Vérifier colonnes
    missing = check_required_columns(df, required)
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return errors

    # Vérification des valeurs
    for index, row in df.iterrows():
        sid = str(row["student_id"]).strip()
        if not sid:
            errors.append(f"Row {index + 2}: Missing student_id")
        gender = str(row["gender (M/F)"]).upper().strip()
        if gender not in ["M", "F"]:
            errors.append(f"Row {index + 2}: Invalid gender '{gender}' (expected M/F)")
    return errors


def validate_teachers_file(file_path, user):
    errors = []
    df = load_dataframe(file_path)
    required = ["first_name", "last_name", "grade", "status", "institute_acronym"]

    missing = check_required_columns(df, required)
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return errors

    # Vérification existence des institutes
    user_institution = user.institution
    valid_acronyms = set(
        Institute.objects.filter(institution=user_institution).values_list(
            "acronym", flat=True
        )
    )

    for index, row in df.iterrows():
        acronym = str(row["institute_acronym"]).strip()
        if acronym not in valid_acronyms:
            errors.append(
                f"Row {index + 2}: Institute '{acronym}' not found for your institution."
            )
    return errors


def validate_programs_file(file_path, user):
    errors = []
    df = load_dataframe(file_path)
    required = ["program_id", "name", "domain", "level", "institute_acronym"]

    missing = check_required_columns(df, required)
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return errors

    user_institution = user.institution
    valid_acronyms = set(
        Institute.objects.filter(institution=user_institution).values_list(
            "acronym", flat=True
        )
    )

    for index, row in df.iterrows():
        acronym = str(row["institute_acronym"]).strip()
        if acronym not in valid_acronyms:
            errors.append(
                f"Row {index + 2}: Unknown institute acronym '{acronym}' for your institution."
            )
    return errors


def validate_courses_file(file_path):
    errors = []
    df = load_dataframe(file_path)
    required = [
        "course_id",
        "code",
        "name",
        "credits",
        "semester",
        "program_id",
        "teacher_id (optional)",
    ]

    missing = check_required_columns(df, required)
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return errors

    program_ids = set(Program.objects.values_list("program_id", flat=True))
    teacher_ids = set(Teacher.objects.values_list("teacher_id", flat=True))

    for index, row in df.iterrows():
        if row["program_id"] not in program_ids:
            errors.append(
                f"Row {index + 2}: Program '{row['program_id']}' does not exist."
            )
        teacher = str(row["teacher_id (optional)"]).strip()
        if teacher and teacher not in teacher_ids:
            errors.append(f"Row {index + 2}: Teacher '{teacher}' not found.")
    return errors


def validate_enrollments_file(file_path, user):
    errors = []
    df = load_dataframe(file_path)
    required = [
        "enrollment_id",
        "student_id",
        "program_id",
        "institute_acronym",
        "academic_year",
        "status",
    ]

    missing = check_required_columns(df, required)
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return errors

    user_institution = user.institution
    valid_acronyms = set(
        Institute.objects.filter(institution=user_institution).values_list(
            "acronym", flat=True
        )
    )
    student_ids = set(Student.objects.values_list("student_id", flat=True))
    program_ids = set(Program.objects.values_list("program_id", flat=True))

    for index, row in df.iterrows():
        acronym = str(row["institute_acronym"]).strip()
        if acronym not in valid_acronyms:
            errors.append(
                f"Row {index + 2}: Institute '{acronym}' not valid for your institution."
            )
        if row["student_id"] not in student_ids:
            errors.append(
                f"Row {index + 2}: Student '{row['student_id']}' does not exist."
            )
        if row["program_id"] not in program_ids:
            errors.append(f"Row {index + 2}: Program '{row['program_id']}' not found.")
    return errors


def validate_results_file(file_path, user):
    errors = []
    df = load_dataframe(file_path)
    required = [
        "result_id",
        "student_id",
        "institute_acronym",
        "course_id",
        "academic_year",
        "session",
        "note",
    ]

    missing = check_required_columns(df, required)
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return errors

    user_institution = user.institution
    valid_acronyms = set(
        Institute.objects.filter(institution=user_institution).values_list(
            "acronym", flat=True
        )
    )
    student_ids = set(Student.objects.values_list("student_id", flat=True))
    course_ids = set(Course.objects.values_list("course_id", flat=True))

    for index, row in df.iterrows():
        if row["student_id"] not in student_ids:
            errors.append(f"Row {index + 2}: Unknown student '{row['student_id']}'")
        acronym = str(row["institute_acronym"]).strip()
        if acronym not in valid_acronyms:
            errors.append(f"Row {index + 2}: Invalid institute acronym '{acronym}'")
        if row["course_id"] not in course_ids:
            errors.append(f"Row {index + 2}: Course '{row['course_id']}' not found.")
        try:
            note = float(row["note"])
            if not (0 <= note <= 20):
                errors.append(
                    f"Row {index + 2}: Invalid note '{note}' (should be between 0 and 20)."
                )
        except Exception:
            errors.append(
                f"Row {index + 2}: Invalid note value '{row['note']}' (must be numeric)."
            )
    return errors


def validate_degrees_file(file_path, user):
    errors = []
    df = load_dataframe(file_path)
    required = [
        "degree_id",
        "student_id",
        "institute_acronym",
        "date_awarded (YYYY-MM-DD)",
        "degree_type",
        "name",
    ]

    missing = check_required_columns(df, required)
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return errors

    user_institution = user.institution
    valid_acronyms = set(
        Institute.objects.filter(institution=user_institution).values_list(
            "acronym", flat=True
        )
    )
    student_ids = set(Student.objects.values_list("student_id", flat=True))

    for index, row in df.iterrows():
        acronym = str(row["institute_acronym"]).strip()
        if acronym not in valid_acronyms:
            errors.append(
                f"Row {index + 2}: Institute '{acronym}' not recognized for your institution."
            )
        if row["student_id"] not in student_ids:
            errors.append(f"Row {index + 2}: Student '{row['student_id']}' not found.")
    return errors
