# coding=utf-8
import datetime
from decimal import Decimal

from bokeh.palettes import Spectral11 as ColorPalette

from time_entry.model import model
from time_entry.view.graph.base_graph import BaseGraph


class TimeVsWorkedHours(BaseGraph):
    def get_title(self):
        return "Gearbeitete Stunden pro Tag"

    @staticmethod
    def get_figure_kwargs() -> dict:
        return {
            "x_axis_type": "datetime"
        }

    def generate(self):
        data = model.get_hours_per_day_for_all_projects()
        all_dates = set()
        for val in data.values():
            for row in val:
                all_dates.add(row[0])
        for val in data.values():
            this_project_dates = set()
            for row in val:
                this_project_dates.add(row[0])
            missing = all_dates - this_project_dates
            for da in missing:
                val.append((da, Decimal("0")))
            val.sort(key=lambda r: r[0])
        project_names = [pro.name for pro in data.keys()]
        source = dict()
        for pro, values in data.items():
            cols = list(zip(*values))
            source[pro.name] = cols[1]
        source["date"] = list(zip(*list(data.values())[0]))[0]
        colors = [*ColorPalette]
        while len(colors) < len(project_names):
            colors.extend(ColorPalette)
        colors = colors[:len(project_names)]
        self.figure.vbar_stack(project_names,
                               x="date",
                               width=datetime.timedelta(hours=18),
                               legend_label=project_names,
                               fill_color=colors,
                               line_color="black",
                               source=source)
