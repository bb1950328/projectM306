# coding=utf-8
from typing import Type, List

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from time_entry.view import base_view
from time_entry.view.graph.base_graph import BaseGraph
from time_entry.view.graph.employee_distribution_for_project import EmployeeDistributionForProject
from time_entry.view.graph.number_of_employees import NumberOfEmployees
from time_entry.view.graph.project_distribution_for_employee import ProjectDistributionForEmployee
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

    def __init__(self, url, cls: Type[BaseGraph]):
        self.name = cls.get_title()
        self.url = url
        self.cls = cls


MENU_ITEMS: List[GraphMenuItem] = [
    GraphMenuItem("time_vs_worked_hours", TimeVsWorkedHours),
    GraphMenuItem("employee_distribution_for_project", EmployeeDistributionForProject),
    GraphMenuItem("project_distribution_for_employee", ProjectDistributionForEmployee),
    GraphMenuItem("number_of_employees", NumberOfEmployees),
]
