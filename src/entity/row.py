# -*- coding: utf-8 -*-
# @Time: 2020/3/18 11:53
# @Author: Rollbear
# @Filename: row.py


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