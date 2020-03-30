# -*- coding: utf-8 -*-
# @Time: 2020/3/18 11:53
# @Author: Rollbear
# @Filename: row.py

from .exceptions import UnKnownField


class Row:
    """记录行"""
    def __init__(self, fields: list, field_names: list):
        """构造方法"""
        self.fields = fields
        self.field_names = field_names

    def __eq__(self, other):
        """判等重载"""
        if self.field_names != other.field_names:
            return False
        if len(self.fields) != len(other.fields):
            return False
        for i in range(len(self.fields)):
            if self.fields[i] != other.fields[i]:
                return False
        return True

    def index(self, field_name: str):
        """定位一个属性的列"""
        if field_name not in self.field_names:
            raise UnKnownField  # 找不到该字段名，则抛出异常
        return self.field_names.index(field_name)

    def __str__(self):
        return str(self.fields)
