# -*- coding: utf-8 -*-
# @Time: 2020/3/16 17:34
# @Author: Rollbear
# @Filename: relation.py

from .exceptions import *
from .row import Row


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
        self.rows.append(Row(fields, self.cols))

    # ---------------------------------------------------
    # --关系代数6个基本操作：并、差、笛卡尔积、选择、投影、更名---
    # ---------------------------------------------------

    def selection(self, key=lambda x: True):
        """根据条件选择记录行"""
        result = Relation(self.cols.copy())
        for row in self.rows:
            if key(row):
                result.add_row(row.fields)
        return result

    def projection(self, col_names: list, repeated_elem=False):
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

        # 去重
        if not repeated_elem:
            tmp = []
            for row in result.rows:
                if row not in tmp:
                    tmp.append(row)
            result.rows = tmp
        return result

    def __mul__(self, other):
        """笛卡尔积
        重载了乘法运算"""
        # todo::笛卡尔积目前不能很好地处理同名属性
        result = Relation(self.cols + other.cols)
        for row in self.rows:
            for other_row in other.rows:
                result.add_row(row.fields + other_row.fields)
        return result

    def __add__(self, other):
        """并运算"""
        # 并运算要满足一些前提，否则抛出异常
        if not isinstance(other, Relation):
            raise UnexpectedRelation

        # 以左操作数为模板对右操作数进行重构
        other.standardizing(pattern=self)

        result = self.copy()
        for row in other.rows:
            if row not in self.rows:
                result.add_row(row.fields)
        return result

    def __sub__(self, other):
        """集合差运算
        重载了减法运算符"""
        # 差运算要满足一些前提，否则抛出异常（与并运算相同）
        if not isinstance(other, Relation):
            raise UnexpectedRelation

        # 以左操作数为模板对右操作数进行重构
        other.standardizing(pattern=self)

        result = self.copy()
        for row in other.rows:
            if row in result.rows:
                result.rows.remove(row)
        return result

    def rename(self, field_name, new_name):
        """
        字段更名
        :param field_name: 旧字段名
        :param new_name: 新字段名
        :return:
        """
        index = self.cols.index(field_name)
        self.cols[index] = new_name
        for row in self.rows:
            row.field_names[index] = new_name
        return self

    # ---------------------------------------------------
    # -----            关系代数的特殊运算              -----
    # ---------------------------------------------------

    def intersection(self, other):
        """交运算"""
        if (not isinstance(other, Relation)) or \
                other.cols != self.cols:
            raise UnexpectedRelation
        result = Relation(self.cols.copy())
        for row in self.rows:
            if row in other.rows:
                result.add_row(row.fields)
        return result

    def natural_join(self, other):
        """自然连接
        自然连接的步骤：
        1.选出公共属性
        2.找出公共属性列完全相同的行
        3.从笛卡尔积中选出这些行"""
        shared_fields = []
        for field in self.cols:
            if field in other.cols:
                shared_fields.append(field)
        # 如果两个关系没有共有属性，那么它们不能自然连接
        if len(shared_fields) == 0:
            raise UnexpectedRelation

        # 从两个关系中投影出公共属性，保留重复行
        self_shared_fields = self.projection(shared_fields, True)
        other_shared_fields = other.projection(shared_fields, True)

        # 挑出那些非共有的属性，进行投影，自然连接的结果中不出现重复的属性
        other_unshared_fields = []
        for field in other.cols:
            if field not in shared_fields:
                other_unshared_fields.append(field)
        other_unshared_fields_projection \
            = other.projection(other_unshared_fields, True)

        result = Relation(self.cols + other_unshared_fields)

        # 行匹配，然后拼接成为最后的经过
        for self_index in range(len(self.rows)):
            for other_index in range(len(other.rows)):
                if self_shared_fields.rows[self_index] \
                        == other_shared_fields.rows[other_index]:
                    result.add_row(
                        self.rows[self_index].fields
                        + other_unshared_fields_projection.rows[other_index].fields)
        return result

    def __truediv__(self, other):
        """
        除运算
        重载了除法运算符，self是前操作数，other为后操作数
        :param other: 除法的第二个操作数
        :return: 一个关系对象
        """
        shared_fields = []
        for field in self.cols:
            if field in other.cols:
                shared_fields.append(field)
        # 如果两个关系没有共有属性，那么它们不能相除
        if len(shared_fields) == 0:
            raise UnexpectedRelation

        # 找出前操作数中不属于共有属性的属性
        self_unshared_fields = []
        for field in self.cols:
            if field not in shared_fields:
                self_unshared_fields.append(field)
        # 将他们投影出来
        self_unshared_cols = self.projection(self_unshared_fields)
        # 投影出后操作数中与前者共有的列
        # other_shared_cols = other.projection(shared_fields)

        total = self_unshared_cols * other
        return self_unshared_cols - (total - self).projection(self_unshared_fields)

    # ---------------------------------------------------
    # -----              其他功能方法                 -----
    # ---------------------------------------------------

    def is_empty(self):
        """判空"""
        return len(self.rows) == 0

    def copy(self):
        """关系对象的深复制"""
        result = Relation(self.cols)
        result.rows = self.rows.copy()
        return result

    def standardizing(self, pattern):
        """根据模板标准化/重构一个关系"""
        # 前提是两个关系拥有相同的字段集，函数通过列的交换，
        # 使得两个关系的字段按相同的顺序排列，以便进行关系代数运算
        if (not isinstance(pattern, Relation)) \
                or (set(self.cols) != set(pattern.cols)):
            raise UnexpectedRelation

        pattern_fields = pattern.cols.copy()
        field_locate = []
        for field in self.cols:
            # 找到当前关系对象的每个字段在模板中的位置
            field_locate.append(pattern_fields.index(field))
        # 将当前关系的字段表和所有行调整为模板中的顺序
        self.cols = pattern_fields
        for row in self.rows:
            row.field_names = pattern_fields
            tmp = row.fields.copy()
            for index in range(len(tmp)):
                tmp[field_locate[index]] = row.fields[index]
            row.fields = tmp
        return self

    def __eq__(self, other):
        """关系对象的判等"""
        return self.cols == other.cols and self.rows == other.rows

    def __str__(self):
        """关系对象的的字符化输出"""
        return str(self.cols)

    def show(self):
        """以表格的方式打印当前关系对象"""
        output = ""
        for field in self.cols:
            output += "{:^10}".format(field)
        # 输出行
        for row in self.rows:
            row_str = ""
            for field in row.fields:
                row_str += "{:^10}".format(field)
            output += ("\n" + row_str)
        print(output)


