# coding=utf-8
import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from time_entry.model import model, util
from time_entry.model.entity import employee
from time_entry.view import base_view


def view(request: WSGIRequest):
    empl_nr = request.GET.get("empl_nr")
    empl = employee.Employee.find(empl_nr)
    absences_list = model.collect_absences(empl_nr)
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
