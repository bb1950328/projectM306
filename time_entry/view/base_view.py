# coding=utf-8
from django.core.handlers.wsgi import WSGIRequest

from time_entry.model.entity import employee


def get_user_context(request: WSGIRequest) -> dict:
    if request.user.is_authenticated:
        empl = employee.Employee.find(request.user.get_username())
        context = {"user": empl,
                   "user_authenticated": True}
    else:
        context = {"user_authenticated": False}
    return context
