# coding=utf-8
from typing import Type, List

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from time_entry.view import base_view
from time_entry.view.graph.base_graph import BaseGraph
from time_entry.view.graph.time_vs_worked_hours import TimeVsWorkedHours


def view(request: WSGIRequest) -> HttpResponse:
    con = {
        **base_view.get_user_context(request),
        "graphs": [{"name": it.name, "url": "graph/" + it.url} for it in MENU_ITEMS]
    }
    return render(request, "graph_list.html", con)


class GraphMenuItem(object):
    name: str
    url: str
    cls: Type[BaseGraph]

    def __init__(self, name, url, cls):
        self.name = name
        self.url = url
        self.cls = cls


MENU_ITEMS: List[GraphMenuItem] = [
    GraphMenuItem("Gearbeitete Stunden pro Tag", "time_vs_worked_hours", TimeVsWorkedHours)
]
