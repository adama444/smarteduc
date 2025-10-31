from django.contrib import admin
from .models import (
    Institution,
    Institute,
    Teacher,
    Program,
    Course,
    Degree,
    Student,
    Enrollment,
    Result,
)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("acronym", "name", "type", "city")
    search_fields = ("name", "acronym", "city")
    list_filter = ("type", "city")


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ("acronym", "name", "institution")
    search_fields = ("name", "acronym")
    list_filter = ("institution",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("program_id", "name", "domain", "level", "institute")
    search_fields = ("program_id", "name", "domain")
    list_filter = ("domain", "level", "institute")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "course_id",
        "code",
        "name",
        "program",
        "teacher",
        "credits",
        "semester",
    )
    search_fields = ("course_id", "code", "name")
    list_filter = ("semester", "program", "teacher")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "first_name", "last_name", "gender", "birthdate")
    search_fields = ("student_id", "first_name", "last_name")
    list_filter = ("gender",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "teacher_id",
        "first_name",
        "last_name",
        "grade",
        "status",
        "institute",
    )
    list_filter = ("grade", "status", "institute")
    search_fields = ("teacher_id", "first_name", "last_name")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "enrollment_id",
        "student",
        "program",
        "institute",
        "academic_year",
        "status",
    )
    list_filter = ("academic_year", "status", "program", "institute")
    search_fields = ("enrollment_id", "student__student_id", "program__name")


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ("degree_id", "name", "degree_type", "enrollment", "date_awarded")
    list_filter = ("degree_type", "date_awarded")
    search_fields = ("degree_id", "name", "enrollment__student__student_id")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "result_id",
        "enrollment",
        "course",
        "academic_year",
        "session",
        "note",
    )
    list_filter = ("academic_year", "session", "course")
    search_fields = ("result_id", "enrollment__student__student_id", "course__code")
