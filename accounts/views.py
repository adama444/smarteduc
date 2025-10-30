from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Vérifier que l'utilisateur est associé à un établissement
            if user.institution is None:
                messages.error(
                    request,
                    "You are not linked to any institution. Contact the administrator.",
                )
                return render(request, "accounts/login.html")

            login(request, user)
            return redirect("core:dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
