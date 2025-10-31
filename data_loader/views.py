from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import ImportFile, ImportLog
from .services import validators, ingestion

# Mapping between file_type and corresponding functions
VALIDATORS = {
    "students": lambda f, u: validators.validate_students_file(f),
    "teachers": validators.validate_teachers_file,
    "programs": validators.validate_programs_file,
    "courses": lambda f, u: validators.validate_courses_file(f),
    "enrollments": validators.validate_enrollments_file,
    "results": validators.validate_results_file,
    "degrees": validators.validate_degrees_file,
}

INGESTORS = {
    "students": lambda f, u: ingestion.ingest_students(f),
    "teachers": ingestion.ingest_teachers,
    "programs": ingestion.ingest_programs,
    "courses": lambda f, u: ingestion.ingest_courses(f),
    "enrollments": ingestion.ingest_enrollments,
    "results": ingestion.ingest_results,
    "degrees": ingestion.ingest_degrees,
}


@login_required
def upload_file(request):
    """
    Main view for uploading and processing data files.
    """
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        file_type = request.POST.get("file_type")

        if file_type not in VALIDATORS:
            messages.error(request, "Invalid file type.")
            return redirect("data_loader:upload")

        # Register file in DB
        import_file = ImportFile.objects.create(
            file=file, file_type=file_type, uploaded_by=request.user
        )

        # Validation
        errors = VALIDATORS[file_type](import_file.file.path, request.user)

        if errors:
            import_file.status = "error"
            import_file.save()
            for e in errors:
                ImportLog.objects.create(
                    import_file=import_file, message=e, is_error=True
                )

            # Formatage des erreurs pour affichage
            error_text = "\n".join([f"- {e}" for e in errors[:5]])
            if len(errors) > 5:
                error_text += f"\n...and {len(errors) - 5} more."

            messages.error(
                request,
                f"File validation failed with {len(errors)} error(s):\n{error_text}",
            )
        else:
            try:
                result_msg = INGESTORS[file_type](import_file.file.path, request.user)
                import_file.status = "validated"
                ImportLog.objects.create(
                    import_file=import_file, message="File successfully ingested."
                )
                messages.success(request, result_msg)
            except Exception as e:
                import_file.status = "error"
                ImportLog.objects.create(
                    import_file=import_file, message=str(e), is_error=True
                )
                messages.error(request, f"An error occurred during import: {str(e)}")
            finally:
                import_file.save()

        return redirect("data_loader:upload")

    # Retrieve import history for the current user
    imports = ImportFile.objects.filter(uploaded_by=request.user).order_by(
        "-uploaded_at"
    )[:10]

    return render(
        request,
        "data_loader/upload.html",
        {
            "imports": imports,
        },
    )
