# coding=utf-8

from time_entry.model import model
from time_entry.view.graph.base_graph import BaseGraph


class NumberOfEmployees(BaseGraph):
    @staticmethod
    def get_figure_kwargs() -> dict:
        return {
            "x_axis_type": "datetime"
        }

    @staticmethod
    def get_title():
        return "Anzahl Mitarbeiter"

    def generate(self, args):
        dates, numbers = model.get_number_of_employees()
        self.figure.line(dates, numbers, line_width=2)
