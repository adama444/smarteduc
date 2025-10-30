from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True)  # e.g., "2024-2025"
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=255)
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="programs"
    )

    def __str__(self):
        return f"{self.name} ({self.institution.name})"


class Course(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="courses"
    )
    credits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")])
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrollments"
    )
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="enrollments"
    )
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.CASCADE, related_name="enrollments"
    )

    class Meta:
        unique_together = ("student", "program", "academic_year")

    def __str__(self):
        return f"{self.student} - {self.program} ({self.academic_year})"


class Result(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="results"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    grade = models.FloatField()

    class Meta:
        unique_together = ("student", "course", "academic_year")

    def __str__(self):
        return f"{self.student} - {self.course.code}: {self.grade}"
