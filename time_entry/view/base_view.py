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


def get_message_context(messages, good_news=False):
    if isinstance(messages, str):
        messages = [messages]
    return {
        "messages": messages,
        "msg_class": "green" if good_news else "red",
        "message_title": "Hinweis" if good_news else "Achtung!",
    }
