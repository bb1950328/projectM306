# coding=utf-8

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from time_entry.model import model
from time_entry.model.entity import employee, project
from time_entry.view import base_view, login, index

ARR_UP = "↑"
ARR_DOWN = "↓"


def table_view(request: WSGIRequest):
    user_empl = employee.Employee.find(request.user.get_username())
    context = {**base_view.get_user_context(request)}
    if not employee.Permission.can_view_project_list(user_empl):
        return redirect(index.no_permission)
    else:
        projects = model.collect_projects()
        for pro in projects:
            pro.hours = round(model.calculate_hours_for_project(pro.nr), 2)
        context.update({
            **base_view.get_user_context(request),
            "projects": projects,
            "updown_arrow_nr": "",
            "updown_arrow_name": "",
            "updown_arrow_hours": "",
            "updown_nr": "asc",
            "updown_name": "asc",
            "updown_hours": "asc",
        })
        sort_projects_list(context, request)

    return render(request, "project_list.html", context=context)


def sort_projects_list(context, request):
    sort = request.GET.get("sort")
    args = sort.split("_") if sort else ["nr", "asc"]
    sort_attr, sort_dir = args
    getters = {
        "nr": lambda e: e.nr,
        "name": lambda e: e.name,
        "hours": lambda e: e.hours,
    }
    context["projects"].sort(key=getters[sort_attr])
    asc = sort_dir == "asc"
    if not asc:
        context["projects"].reverse()
    context["updown_arrow_" + sort_attr] = ARR_DOWN if asc else ARR_UP
    context["updown_" + sort_attr] = "desc" if asc else "asc"


def view(request: WSGIRequest):
    if not request.user.is_authenticated:
        return redirect(login.login)
    project_nr = request.GET.get("project_nr")
    if project_nr:
        return detail_view(int(project_nr), request)
    else:
        return table_view(request)


def detail_view(project_nr, request):
    pro = project.Project.find(project_nr)
    user_empl = employee.Employee.find(request.user.get_username())
    context = base_view.get_user_context(request)
    if employee.Permission.can_view_project_details(user_empl):
        context.update({**base_view.get_user_context(request),
                        "nr": pro.nr,
                        "name": pro.name,
                        "hours": round(model.calculate_hours_for_project(pro.nr), 2),
                        "contributors": [e.firstName + " " + e.lastName for e in
                                         model.get_contributors_for_project(pro.nr)]
                        })
    else:
        return redirect(index.no_permission)
    return render(request, "project.html", context=context)
