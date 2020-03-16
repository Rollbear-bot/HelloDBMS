# -*- coding: utf-8 -*-
# @Time: 2020/3/16 17:48
# @Author: Rollbear
# @Filename: exceptions.py


class UnexpectedCol(Exception):
    """不正确的属性列"""
    def __str__(self):
        return "不正确的属性列"


class UnexpectedRow(Exception):
    """不正确的记录行"""
    def __str__(self):
        return "不正确的记录行"


class RowNoFound(Exception):
    """找不到指定记录"""
    def __str__(self):
        return "找不到指定记录"
