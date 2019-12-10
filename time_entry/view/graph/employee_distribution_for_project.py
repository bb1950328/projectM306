# coding=utf-8
import math
from typing import List

from bokeh.palettes import Spectral11 as ColorPalette
from bokeh.transform import cumsum

from time_entry.model import model, util
from time_entry.model.entity.employee import Employee
from time_entry.view.graph.base_graph import BaseGraph


class EmployeeDistributionForProject(BaseGraph):

    @staticmethod
    def get_figure_kwargs() -> dict:
        return {
            "tools": "hover",
            "tooltips": "@empl_name: @hours Stunden",
        }

    @staticmethod
    def get_title():
        return "Stundenverteilung nach Mitarbeiter"

    @staticmethod
    def get_argument_keys() -> List[str]:
        return ["Projektnummer"]

    def generate(self, args):
        data = self.get_data_dict(args)
        source = {
            "empl_name": [],
            "hours": [],
        }
        for empl, hours in data.items():
            source["empl_name"].append(self.get_display_name_for_key_entity(empl))
            source["hours"].append(float(hours))
        hour_sum = sum(source["hours"])
        source["angle"] = [hours / hour_sum * 2 * math.pi for hours in source["hours"]]
        source["color"] = util.repeat_maxlen(ColorPalette, len(source["hours"]))
        self.figure.wedge(x=0,
                          y=1,
                          radius=0.4,
                          start_angle=cumsum("angle", include_zero=True),
                          end_angle=cumsum("angle"),
                          line_color="black",
                          fill_color="color",
                          legend="empl_name",
                          source=source,
                          )

    @staticmethod
    def get_display_name_for_key_entity(empl: Employee):
        return empl.firstName + " " + empl.lastName

    def get_data_dict(self, args):
        project_nr = int(args.get(self.get_argument_keys()[0]))
        data = model.get_hours_per_employee_for_project(project_nr)
        return data
