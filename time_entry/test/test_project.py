from unittest import TestCase

# coding=utf-8
from time_entry.model.project import Project


class TestProject(TestCase):
    def test_adapter_converter(self):
        project = Project()
        project.nr = 12345
        project.name = "TestProject"
        project.description = "It's just a test."
        out = Project.adapter(project)
        project2 = Project.converter(bytes(out, "UTF-8", "replace"))
        self.assertEqual(project.nr, project2.nr)
        self.assertEqual(project.name, project2.name)
        self.assertEqual(project.description, project2.description)

    def test_properties_nr_1(self):
        project = Project()

        try:
            project.nr = 1
        except ValueError:
            self.fail()

    def test_properties_nr_2(self):
        project = Project()

        try:
            project.nr = 0
        except ValueError:
            pass
        else:
            self.fail()

    def test_properties_nr_3(self):
        project = Project()

        try:
            project.nr = -1
        except ValueError:
            pass
        else:
            self.fail()

    def test_properties_name_1(self):
        project = Project()

        try:
            project.name = "ABCdefgHIJK"
        except ValueError:
            self.fail()

    def test_properties_name_2(self):
        project = Project()

        try:
            project.name = "Bad;Name"
        except ValueError:
            pass
        else:
            self.fail()

    def test_properties_description_1(self):
        project = Project()

        try:
            project.description = "QWERTZUIOPasdfghjklYXCVBNM"
        except ValueError:
            self.fail()

    def test_properties_description_2(self):
        project = Project()

        try:
            project.description = "Bad;Description"
        except ValueError:
            pass
        else:
            self.fail()
