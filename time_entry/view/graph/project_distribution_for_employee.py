# coding=utf-8
from typing import List

from time_entry.model import model
from time_entry.model.entity.project import Project
from time_entry.view.graph.employee_distribution_for_project import EmployeeDistributionForProject


class ProjectDistributionForEmployee(EmployeeDistributionForProject):

    @staticmethod
    def get_title():
        return "Stundenverteilung nach Projekt"

    @staticmethod
    def get_argument_keys() -> List[str]:
        return ["Mitarbeiternummer"]

    @staticmethod
    def get_display_name_for_key_entity(project: Project):
        return project.name

    def get_data_dict(self, args):
        empl_nr = int(args.get(self.get_argument_keys()[0]))
        data = model.get_hours_per_project_for_employee(empl_nr)
        return data
