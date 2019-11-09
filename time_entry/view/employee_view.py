# coding=utf-8
import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from time_entry.model import model, util
from time_entry.model.entity import employee
from time_entry.view import base_view

ARR_UP = "↑"
ARR_DOWN = "↓"


def table_view(request: WSGIRequest):
    employees = model.collect_employees()
    for empl in employees:
        empl.floatTime = round(model.calculate_float_time(empl.emplNr), 2)
    context = {
        **base_view.get_user_context(request),
        "employees": employees,
        "updown_arrow_nr": "",
        "updown_arrow_firstname": "",
        "updown_arrow_lastname": "",
        "updown_arrow_ftime": "",
        "updown_nr": "asc",
        "updown_firstname": "asc",
        "updown_lastname": "asc",
        "updown_ftime": "asc",
    }
    sort = request.GET.get("sort")
    args = sort.split("_") if sort else ["nr", "asc"]
    sort_attr, sort_dir = args

    getters = {
        "nr": lambda e: e.emplNr,
        "firstname": lambda e: e.firstName,
        "lastname": lambda e: e.lastName,
        "ftime": lambda e: e.floatTime,
    }
    employees.sort(key=getters[sort_attr])
    asc = sort_dir == "asc"
    if not asc:
        employees.reverse()

    context["updown_arrow_" + sort_attr] = ARR_DOWN if asc else ARR_UP
    context["updown_" + sort_attr] = "desc" if asc else "asc"

    return render(request, "employee_list.html", context=context)


def view(request: WSGIRequest):
    empl_nr = request.GET.get("empl_nr")
    if empl_nr:
        return detail_view(empl_nr, request)
    else:
        return table_view(request)


def detail_view(empl_nr, request):
    empl = employee.Employee.find(empl_nr)
    absences_list = model.collect_absences(empl_nr, sort=True)
    absences = []
    for ab in absences_list:
        aab = {
            "start": util.locale_format(ab.start),
            "end": util.locale_format(ab.end),
            "reason": ab.reason,
            "length": ab.length,
        }
        absences.append(aab)
    context = {**base_view.get_user_context(request),
               "firstName": empl.firstName,
               "lastName": empl.lastName,
               "empl_nr": empl.emplNr,
               "float_time_total": round(model.calculate_float_time(empl_nr), 2),
               "active_since": util.locale_format(empl.since),
               "active_until": util.locale_format(empl.until) if empl.until else "",
               "absence_total": model.count_absent_days(empl_nr),
               "absences": absences,
               }
    return render(request, "employee.html", context=context)


def new_absence(request: WSGIRequest):
    today = datetime.date.today().isoformat()
    context = {
        **base_view.get_user_context(request),
        "default_empl_nr": request.GET.get("empl_nr", "0"),
        "default_start": today,
        "default_end": today,
    }
    if request.POST:
        try:
            model.add_absence(request.POST)
        except ValueError as e:
            msg = "Fehler: " + " ".join(e.args)
            good_news = False
        else:
            msg = "Die Absenz wurde erfolgreich gespeichert."
            good_news = True
        context.update(base_view.get_message_context(msg, good_news))
    return render(request, "new_absence.html", context)
