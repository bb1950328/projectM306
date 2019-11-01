# coding=utf-8
from django.shortcuts import render


def index(request):
    context = {
        "user": {"firstName": "Basil",
                 "lastName": "Bader"}
    }
    return render(request, "index.html", context)
