from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.acronym} - {self.name}"


class Institute(models.Model):
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="institutes"
    )
    name = models.CharField(max_length=150)
    acronym = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.acronym} ({self.institution.acronym})"


class Program(models.Model):
    program_id = models.CharField(max_length=20, primary_key=True)
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name="programs"
    )
    name = models.CharField(max_length=150)
    domain = models.CharField(max_length=100)
    level = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.level})"


class Student(models.Model):
    student_id = models.CharField(max_length=20, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")])
    birthdate = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("abandoned", "Abandoned"),
        ("graduated", "Graduated"),
    ]

    enrollment_id = models.CharField(max_length=20, primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrollments"
    )
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="enrollments"
    )
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=20)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="active")

    def __str__(self):
        return f"{self.student} - {self.program} ({self.academic_year})"


class Teacher(models.Model):
    STATUS_CHOICES = [
        ("permanent", "Permanent"),
        ("vacataire", "Vacataire"),
        ("contractuel", "Contractuel"),
    ]
    GRADE_CHOICES = [
        ("assistant", "Assistant"),
        ("maitre_assistant", "Maître Assistant"),
        ("maitre_de_conferences", "Maître de Conférences"),
        ("professeur", "Professeur Titulaire"),
        ("docteur", "Docteur"),
        ("autre", "Autre"),
    ]

    teacher_id = models.CharField(max_length=20, primary_key=True)
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name="teachers"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES, default="docteur")
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="permanent"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.grade})"


class Course(models.Model):
    course_id = models.CharField(max_length=20, primary_key=True)
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="courses"
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    credits = models.PositiveIntegerField()
    semester = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Degree(models.Model):
    DEGREE_TYPE_CHOICES = [
        ("licence_fondamentale", "Licence Fondamentale"),
        ("licence_pro", "Licence Professionnelle"),
        ("bachelor", "Bachelor"),
        ("master_recherche", "Master de Recherche"),
        ("master_pro", "Master Professionnel"),
        ("phd", "PhD / Doctorate"),
        ("bts", "BTS"),
    ]

    degree_id = models.CharField(max_length=20, primary_key=True)
    enrollment = models.OneToOneField(
        Enrollment, on_delete=models.CASCADE, related_name="degree"
    )
    date_awarded = models.DateField()
    degree_type = models.CharField(max_length=100, choices=DEGREE_TYPE_CHOICES)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.degree_type})"


class Result(models.Model):
    SESSION_CHOICES = [
        ("normal", "Session Normale"),
        ("rattrapage", "Session de Rattrapage"),
    ]

    result_id = models.CharField(max_length=20, primary_key=True)
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="results"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="results")
    academic_year = models.CharField(max_length=20)
    session = models.CharField(max_length=50, choices=SESSION_CHOICES, default="normal")
    note = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.enrollment.student} - {self.course.code} ({self.note})"
