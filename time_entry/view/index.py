# coding=utf-8
import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

# TODO https://docs.djangoproject.com/en/2.2/topics/auth/default/#authentication-in-web-requests
from time_entry.model import model
from time_entry.view import base_view, login


def index(request: WSGIRequest):
    if not request.user.is_authenticated:
        return redirect(login.login)
    context = {
        **base_view.get_user_context(request),
        **generate_entries_context(request.user.get_username(), request.GET),
    }
    return render(request, "index.html", context)


def generate_entries_context(empl_nr: int, GET) -> dict:
    mode = GET.get("mode")
    now = datetime.datetime.now()
    if mode is None:
        year = now.year
        month = now.month
        mode = "m"
    else:
        year = int(GET.get("year"))
        if mode.startswith("m"):
            mode = "m"
            month = int(GET.get("month"))
        elif mode.startswith("w"):
            mode = "w"
            week = int(GET.get("week"))
    if mode == "m":
        start = datetime.datetime(year, month, 1)
        mp1 = month + 1
        yp1 = year
        if mp1 == 13:
            mp1 = 1
            yp1 += 1
        end = start.replace(month=mp1, year=yp1)
    else:
        start = datetime.datetime.strptime(f"{year}_{week - 1}_1", "%Y_%W_%w")  # python week numbers start from 0
        end = start + datetime.timedelta(days=7)

    entries = model.collect_entries(empl_nr, start, end)
    days = {}
    for entry in entries:
        day = entry.start.date()

        con = {"project_nr": entry.getProject().nr,
               "project_name": entry.getProject().name,
               "von": entry.start.strftime("%H:%M"),
               "bis": entry.end.strftime("%H:%M"),
               "id": entry.id,
               }
        try:
            days[day].append(con)
        except KeyError:
            days[day] = [con]
    context = {"days": [],
               "now": now,
               "selection": {
                   "value_month": "selected" if mode == "m" else "",
                   "value_week": "selected" if mode == "w" else "",
                   "week_or_month": month if mode == "m" else week,
                   "year": year,
                   "max_value": 12 if mode == "m" else 52,
                   "default_month": now.month,
                   "default_week": int(now.date().strftime("%W")),
                   "default_year": now.year,
               }}
    for day, entries in days.items():
        context["days"].append(
            {"id": day.isoformat(),
             "displayName": day.strftime("%a, %d.%m.%Y"),
             "entries": entries})
    return context
