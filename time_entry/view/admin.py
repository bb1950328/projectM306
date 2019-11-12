# coding=utf-8
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from time_entry.model import admin as model_admin


def admin(request: WSGIRequest):
    con = {
        "git_log": model_admin.get_git_log()
    }
    return render(request, "admin.html", context=con)


def git_pull(request: WSGIRequest):
    return HttpResponse("#TODO", "text/plain")
