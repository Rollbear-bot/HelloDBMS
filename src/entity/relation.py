# -*- coding: utf-8 -*-
# @Time: 2020/3/16 17:34
# @Author: Rollbear
# @Filename: relation.py

from .exceptions import UnexpectedCol, UnexpectedRow, RowNoFound

'''
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

    def get_row(self, index: int):
        """获取一条记录"""
        # 表空或者index指向不存在的记录时抛出异常
        if len(self.cols) == 0 or index >= len(self.cols[0].rows):
            raise RowNoFound
        result = list(range(len(self.cols)))
        for count in range(len(self.cols)):
            result[count] = self.cols[count].rows[index]
        return result

    def switch_row(self, key):
        """
        选择行
        :param key: 选择条件
        :return: 返回新的关系
        """
'''


class Row:
    """记录行"""
    def __init__(self, fields: list):
        """构造方法"""
        self.fields = fields


class Relation2(object):
    """关系类"""
    def __init__(self):
        """构造方法"""
        self.rows = []  # 用一个列表来存放记录行
        self.cols = []  # 属性名

    def add_col(self, col_name: str, rows: list):
        """向关系中添加一个属性列"""
        if len(rows) != len(self.rows):
            raise UnexpectedCol
        self.cols.append(col_name)
        index = 0
        # 向已存在的行中添加新字段
        for row in self.rows:
            row.fields.append(rows[index])
            index += 1

    def add_row(self, fields: list):
        """向关系中添加一条记录行"""
        if len(self.rows) != 0 and \
                len(fields) != len(self.rows[0].fields):
            raise UnexpectedRow
        self.rows.append(Row(fields))

    def switch_rows(self, key=lambda x: True):
        """根据条件选择记录行"""
        result = Relation2()
        result.cols = self.cols.copy()
        for row in self.rows:
            if key(row):
                result.add_row(row.fields)
        return result

    def projection(self, col_names: list):
        """投影"""
        # 检查是否包含不存在的属性
        for item in col_names:
            if item not in self.cols:
                raise UnexpectedCol

        result = Relation2()
        result.cols = col_names
        for row in self.rows:
            fields = []
            for field in col_names:
                if field in self.cols:
                    fields.append(row.fields[self.cols.index(field)])
            result.add_row(fields)
        return result

    def is_empty(self):
        """判空"""
        return len(self.rows) == 0
