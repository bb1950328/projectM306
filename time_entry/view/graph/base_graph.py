# coding=utf-8
from abc import ABC, abstractmethod

from bokeh.embed import file_html
from bokeh.plotting import figure
from bokeh.resources import CDN
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from time_entry.model.entity import employee
from time_entry.view import login, index, base_view


class BaseGraph(ABC):
    def __init__(self):
        self.figure = figure(plot_width=1280, plot_height=720, title=self.get_title(), **self.get_figure_kwargs())

    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def generate(self):
        pass

    @staticmethod
    def get_figure_kwargs() -> dict:
        return {}

    def save(self):
        return file_html(self.figure, CDN, self.get_title())

    @classmethod
    def view(cls, request: WSGIRequest) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect(login.login)
        user_empl = employee.Employee.find(request.user.get_username())
        if not employee.Permission.can_view_graphs(user_empl):
            return redirect(index.no_permission)
        self = cls()
        self.generate()
        graph_html = self.save()
        graph_html = graph_html.replace("https://cdn.pydata.org/bokeh/release/bokeh-1.4.0.min.js",
                                        "/static/js/bokeh-1.4.0.min.js")
        con = {
            **base_view.get_user_context(request),
            "graph_title": self.get_title(),
            "graph_html": mark_safe(graph_html)
        }
        return render(request, "graph.html", context=con)
