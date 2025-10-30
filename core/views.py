from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Student, Institution, Program, Course, Enrollment, Result


@login_required
def dashboard(request):
    """
    Main dashboard displaying summary statistics
    """
    context = {
        "total_students": Student.objects.count(),
        "total_institutions": Institution.objects.count(),
        "total_programs": Program.objects.count(),
        "total_courses": Course.objects.count(),
        "total_enrollments": Enrollment.objects.count(),
        "total_results": Result.objects.count(),
    }
    return render(request, "core/dashboard.html", context)
