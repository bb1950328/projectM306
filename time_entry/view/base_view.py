# coding=utf-8
from django.core.handlers.wsgi import WSGIRequest

from time_entry.model.entity import employee


def get_user_context(request: WSGIRequest) -> dict:
    if request.user.is_authenticated:
        empl = employee.Employee.find(request.user.get_username())
        context = {"user": empl,
                   "user_authenticated": True}

        def get_dict(text, link):
            return {"text": text, "link": link}

        nav_elements = [
            get_dict("Home", "index.html"),
        ]
        if employee.Permission.can_view_employee_list(empl):
            nav_elements.append(get_dict("Mitarbeiter", "employee.html"))
        if employee.Permission.can_be_admin(empl):
            nav_elements.append(get_dict("Admin", "admin.html"))
        if employee.Permission.can_view_project_list(empl):
            nav_elements.append(get_dict("Projekte", "project.html"))
        context["nav_elements"] = nav_elements
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
