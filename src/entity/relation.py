# -*- coding: utf-8 -*-
# @Time: 2020/3/16 17:34
# @Author: Rollbear
# @Filename: relation.py
from .exceptions import UnexpectedCol, UnexpectedRow


class Column:
    """属性列类"""
    def __init__(self, col_name, rows: list):
        self.col_name = col_name  # 属性名
        self.rows = rows  # 所有行位于该列的值


class Relation(object):
    """关系类"""
    def __init__(self):
        self.cols = []  # 关系的属性

    def add_col(self, col_name: str, rows: list):
        """向关系中添加一个属性"""
        self.cols.append(Column(col_name, rows))
        # 如果新添加的属性的行数与已存在的属性的行数不等，抛出异常
        if len(self.cols) > 0 and len(self.cols[0].rows) != len(rows):
            raise UnexpectedCol

    def add_row(self, row: list):
        """向关系中添加一行记录"""
        # 如果记录的长度和关系中属性的个数不等，抛出异常
        if len(self.cols) != len(row):
            raise UnexpectedRow
        # 向关系中添加行
        for count in range(len(row)):
            self.cols[count].rows.append(row[count])

