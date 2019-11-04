# coding=utf-8
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from time_entry.model import model, util
from time_entry.model.entity import employee
from time_entry.view import base_view


def view(request: WSGIRequest):
    empl_nr = request.GET.get("empl_nr")
    empl = employee.Employee.find(empl_nr)
    context = {**base_view.get_user_context(request),
               "firstName": empl.firstName,
               "lastName": empl.lastName,
               "float_time_total": round(model.calculate_float_time(empl_nr), 2),
               "active_since": util.locale_format(empl.since),
               "active_until": util.locale_format(empl.until) if empl.until else "",
               }
    return render(request, "employee.html", context=context)
