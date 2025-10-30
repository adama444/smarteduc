import pandas as pd
from core.models import Student, Program, Course, Institution, AcademicYear


def _read_file(file_path):
    """Read file (CSV or Excel) using pandas"""
    if file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        return pd.read_excel(file_path)
    return pd.read_csv(file_path)


# ------------- STUDENTS -------------
def validate_students_file(file_path):
    errors = []
    try:
        df = _read_file(file_path)
        required_columns = [
            "student_id",
            "first_name",
            "last_name",
            "gender",
            "birth_date",
            "institution_code",
        ]
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            errors.append(f"Missing columns: {', '.join(missing)}")

        if df["student_id"].duplicated().any():
            errors.append("Duplicate student_id values found.")

        if not df["gender"].isin(["M", "F"]).all():
            errors.append("Invalid gender values (must be 'M' or 'F').")

        for code in df["institution_code"].unique():
            if not Institution.objects.filter(code=code).exists():
                errors.append(f"Institution with code '{code}' not found.")

    except Exception as e:
        errors.append(str(e))
    return errors


# ------------- PROGRAMS -------------
def validate_programs_file(file_path):
    errors = []
    try:
        df = _read_file(file_path)
        required_columns = ["program_name", "institution_code"]
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            errors.append(f"Missing columns: {', '.join(missing)}")

        for code in df["institution_code"].unique():
            if not Institution.objects.filter(code=code).exists():
                errors.append(f"Institution with code '{code}' not found.")

        if df.duplicated(subset=["program_name", "institution_code"]).any():
            errors.append("Duplicate programs per institution found.")

    except Exception as e:
        errors.append(str(e))
    return errors


# ------------- COURSES -------------
def validate_courses_file(file_path):
    errors = []
    try:
        df = _read_file(file_path)
        required_columns = [
            "course_code",
            "course_name",
            "program_name",
            "institution_code",
            "credits",
        ]
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            errors.append(f"Missing columns: {', '.join(missing)}")

        for code in df["institution_code"].unique():
            if not Institution.objects.filter(code=code).exists():
                errors.append(f"Institution with code '{code}' not found.")

    except Exception as e:
        errors.append(str(e))
    return errors


# ------------- ENROLLMENTS -------------
def validate_enrollments_file(file_path):
    errors = []
    try:
        df = _read_file(file_path)
        required_columns = ["student_id", "program_name", "academic_year"]
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            errors.append(f"Missing columns: {', '.join(missing)}")

        for sid in df["student_id"].unique():
            if not Student.objects.filter(student_id=sid).exists():
                errors.append(f"Student '{sid}' not found.")

        for pname in df["program_name"].unique():
            if not Program.objects.filter(name=pname).exists():
                errors.append(f"Program '{pname}' not found.")

        for ay in df["academic_year"].unique():
            if not AcademicYear.objects.filter(name=ay).exists():
                errors.append(f"Academic year '{ay}' not found.")

    except Exception as e:
        errors.append(str(e))
    return errors


# ------------- RESULTS -------------
def validate_results_file(file_path):
    errors = []
    try:
        df = _read_file(file_path)
        required_columns = ["student_id", "course_code", "academic_year", "grade"]
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            errors.append(f"Missing columns: {', '.join(missing)}")

        for sid in df["student_id"].unique():
            if not Student.objects.filter(student_id=sid).exists():
                errors.append(f"Student '{sid}' not found.")

        for ccode in df["course_code"].unique():
            if not Course.objects.filter(code=ccode).exists():
                errors.append(f"Course '{ccode}' not found.")

        for ay in df["academic_year"].unique():
            if not AcademicYear.objects.filter(name=ay).exists():
                errors.append(f"Academic year '{ay}' not found.")

    except Exception as e:
        errors.append(str(e))
    return errors
