# coding=utf-8
from time_entry.view.graph.base_graph import BaseGraph


class TestGraph(BaseGraph):
    @staticmethod
    def get_title():
        return "Test Graph"

    def generate(self, args):
        squares_x = [1, 3, 4, 5, 8]
        squares_y = [8, 7, 3, 1, 10]
        circles_x = [9, 12, 4, 3, 15]
        circles_y = [8, 4, 11, 6, 10]

        self.figure.square(squares_x, squares_y, size=12, color='navy', alpha=0.6)
        self.figure.circle(circles_x, circles_y, size=12, color='red')
