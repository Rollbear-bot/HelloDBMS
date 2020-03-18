# -*- coding: utf-8 -*-
# @Time: 2020/3/16 17:34
# @Author: Rollbear
# @Filename: relation.py

from .exceptions import *


class Row:
    """记录行"""
    def __init__(self, fields: list):
        """构造方法"""
        self.fields = fields

    def __eq__(self, other):
        """判等重载"""
        if len(self.fields) != len(other.fields):
            return False
        for i in range(len(self.fields)):
            if self.fields[i] != other.fields[i]:
                return False
        return True

    def __str__(self):
        return str(self.fields)


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

    # -----关系代数5个基本操作：并、差、笛卡尔积、选择、投影-----

    def switch_rows(self, key=lambda x: True):
        """根据条件选择记录行"""
        result = Relation(self.cols.copy())
        for row in self.rows:
            if key(row):
                result.add_row(row.fields)
        return result

    def cartesian_product(self):
        """笛卡尔积"""
        pass

    def projection(self, col_names: list):
        """投影"""
        # 检查是否包含不存在的属性
        for item in col_names:
            if item not in self.cols:
                raise UnexpectedCol

        result = Relation(col_names.copy())
        result.cols = col_names
        for row in self.rows:
            fields = []
            for field in col_names:
                if field in self.cols:
                    fields.append(row.fields[self.cols.index(field)])
            result.add_row(fields)
        return result

    def union(self, other):
        """并运算"""
        # 并运算要满足一些前提，否则抛出异常
        if (not isinstance(other, Relation)) or \
                other.cols != self.cols:
            raise UnexpectedRelation

        result = self.__copy__()
        for row in other.rows:
            if row not in self.rows:
                result.add_row(row.fields)
        return result

    def __sub__(self, other):
        """集合差运算
        重载了减法运算符"""
        # 差运算要满足一些前提，否则抛出异常（与并运算相同）
        if (not isinstance(other, Relation)) or \
                other.cols != self.cols:
            raise UnexpectedRelation

        result = self.__copy__()
        for row in other.rows:
            if row in result.rows:
                result.rows.remove(row)
        return result

    # -----其他功能方法-----

    def set_field_names(self, field_names: list):
        """一次性设置多个属性名"""
        pass

    def is_empty(self):
        """判空"""
        return len(self.rows) == 0

    def __copy__(self):
        result = Relation(self.cols)
        result.rows = self.rows.copy()
        return result


