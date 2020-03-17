# -*- coding: utf-8 -*-
# @Time: 2020/3/16 17:34
# @Author: Rollbear
# @Filename: relation.py

from .exceptions import UnexpectedCol, UnexpectedRow, RowNoFound


class Row:
    """记录行"""
    def __init__(self, fields: list):
        """构造方法"""
        self.fields = fields


class Relation(object):
    """关系类"""
    def __init__(self, field_names):
        """构造方法"""
        self.rows = []  # 用一个列表来存放记录行
        self.cols = field_names  # 属性名

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
        if len(self.cols) != 0 and len(fields) != len(self.cols):
            raise UnexpectedRow
        if len(self.rows) != 0 and \
                len(fields) != len(self.rows[0].fields):
            raise UnexpectedRow
        self.rows.append(Row(fields))

    def switch_rows(self, key=lambda x: True):
        """根据条件选择记录行"""
        result = Relation()
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

        result = Relation()
        result.cols = col_names
        for row in self.rows:
            fields = []
            for field in col_names:
                if field in self.cols:
                    fields.append(row.fields[self.cols.index(field)])
            result.add_row(fields)
        return result

    def set_field_names(self, field_names: list):
        """一次性设置多个属性名"""
        pass

    def is_empty(self):
        """判空"""
        return len(self.rows) == 0
