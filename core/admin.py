from django.contrib import admin
from .models import (
    Institution,
    AcademicYear,
    Program,
    Course,
    Student,
    Enrollment,
    Result,
)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "email", "phone")
    search_fields = ("name", "code")


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "institution")
    list_filter = ("institution",)
    search_fields = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "program", "credits")
    list_filter = ("program",)
    search_fields = ("code", "name")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "first_name", "last_name", "gender")
    list_filter = ("gender",)
    search_fields = ("student_id", "first_name", "last_name")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "program", "academic_year")
    list_filter = ("program", "academic_year")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "academic_year", "grade")
    list_filter = ("academic_year", "course")
    search_fields = ("student__student_id", "course__code")
