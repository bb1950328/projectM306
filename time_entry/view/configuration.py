from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from time_entry.model.entity.setting import Setting
from time_entry.view import base_view


def view(request: WSGIRequest):
    se = [
        {
            "id": Setting.SOLL_WORK_PER_DAY,
            "displayName": "Sollstunden pro Tag",
            "value": Setting.find_float_value(Setting.SOLL_WORK_PER_DAY),
            "type": "number",
        },
        {
            "id": Setting.MAX_WORK_PER_DAY,
            "displayName": "Maximale Arbeitsstunden pro Tag",
            "value": Setting.find_float_value(Setting.MAX_WORK_PER_DAY),
            "type": "number",
        }
    ]
    context = {
        **base_view.get_user_context(request),
        "all_settings": se,
    }
    return render(request, "configuration.html", context=context)


def save(request: WSGIRequest):
    print("save", request.GET)
    for const, value in request.GET.items():
        se = Setting.find(const)
        if value.startswith('"'):
            value = value[1:-1]
        se.value = value
        se.save()
    return redirect(view)
