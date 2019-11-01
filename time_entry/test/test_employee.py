from unittest import TestCase

# coding=utf-8
from time_entry.model.employee import Employee


class TestEmployee(TestCase):
    def test_adapter_converter(self):
        empl = Employee()
        empl.emplNr = 123
        empl.firstName = "Donald"
        empl.lastName = "Duck"
        out = Employee.adapter(empl)
        empl2 = Employee.converter(bytes(out, "UTF-8", "replace"))
        self.assertEqual(empl.emplNr, empl2.emplNr)
        self.assertEqual(empl.firstName, empl2.firstName)
        self.assertEqual(empl.lastName, empl2.lastName)

    def test_properties_emplNr_1(self):
        empl = Employee()

        try:
            empl.emplNr = 1
        except ValueError:
            self.fail()

    def test_properties_emplNr_2(self):
        empl = Employee()

        try:
            empl.emplNr = 0
        except ValueError:
            pass
        else:
            self.fail()

    def test_properties_emplNr_3(self):
        empl = Employee()

        try:
            empl.emplNr = -1
        except ValueError:
            pass
        else:
            self.fail()

    def test_properties_firstName_1(self):
        empl = Employee()

        try:
            empl.firstName = "Donald"
        except ValueError:
            self.fail()

    def test_properties_firstName_2(self):
        empl = Employee()

        try:
            empl.firstName = "Not;Allowed"
        except ValueError:
            pass
        else:
            self.fail()

    def test_properties_lastName_1(self):
        empl = Employee()

        try:
            empl.lastName = "Duck"
        except ValueError:
            self.fail()

    def test_properties_lastName_2(self):
        empl = Employee()

        try:
            empl.lastName = "Not;Allowed"
        except ValueError:
            pass
        else:
            self.fail()
