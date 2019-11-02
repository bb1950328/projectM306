# coding=utf-8
from django.contrib import auth
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect


def login(request: WSGIRequest):
    context = {"message": ""}
    if len(request.POST):
        user = auth.authenticate(request, username=request.POST["employee_number"], password=request.POST["password"])
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            context["message"] = "Benutzername oder Passwort ist falsch!"
    return render(request, "login.html", context=context)


def logout(request: WSGIRequest):
    from time_entry.model.entity.employee import Employee
    context = {}
    if request.user.is_authenticated:
        empl = Employee.find(int(request.user.get_username()))
        context["message"] = f"{empl.firstName} {empl.lastName}, Sie wurden ausgeloggt."
    else:
        context["message"] = "Niemand war eingeloggt."
    auth.logout(request)
    return render(request, "logout.html", context=context)
