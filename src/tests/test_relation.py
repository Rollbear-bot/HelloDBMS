# -*- coding: utf-8 -*-
# @Time: 2020/3/17 10:38
# @Author: Rollbear
# @Filename: test_relation.py

import unittest

from entity.relation import *
from entity.exceptions import *


def create_tmp_relation():
    result = Relation(['id', 'name', 'score'])
    result.add_row([1, 'John', 99])
    result.add_row([2, 'Sally', 98])
    result.add_row([3, 'Tom', 80])
    return result


class TestRelation(unittest.TestCase):
    """测试类"""

    def test_switch_one_row(self):
        """对行选取方法的测试"""
        r = create_tmp_relation()
        result = r.switch_rows(lambda x: x.fields[1] == 'Tom')
        self.assertEqual(len(result.rows), 1)
        self.assertListEqual(result.cols, ['id', 'name', 'score'])
        self.assertListEqual(result.rows[0].fields, [3, 'Tom', 80])

    def test_switch_two_rows(self):
        """测试从关系中选取两行"""
        r = create_tmp_relation()
        result = r.switch_rows(lambda x: x.fields[2] > 90)
        self.assertEqual(len(result.rows), 2)
        self.assertListEqual(result.cols, ['id', 'name', 'score'])
        self.assertListEqual(result.rows[0].fields, [1, 'John', 99])
        self.assertListEqual(result.rows[1].fields, [2, 'Sally', 98])

    def test_switch_None(self):
        """测试所有行不满足条件时"""
        r = create_tmp_relation()
        result = r.switch_rows(lambda x: x.fields[2] > 100)
        self.assertEqual(len(result.rows), 0)
        self.assertFalse(not result.is_empty())

    def test_projection(self):
        """测试关系的投影"""
        r = create_tmp_relation()
        result = r.projection(['name'])
        self.assertEqual(len(result.rows), 3)
        self.assertListEqual(result.cols, ['name'])
        self.assertListEqual(result.rows[0].fields, ['John'])

    def test_two_cols_projection(self):
        """测试投影两行"""
        r = create_tmp_relation()
        result = r.projection(['name', 'id'])
        self.assertEqual(len(result.rows), 3)
        self.assertListEqual(result.cols, ['name', 'id'])
        self.assertListEqual(result.rows[0].fields, ['John', 1])

    def test_invalid_col_projection(self):
        """测试投影出空集的情况"""
        r = create_tmp_relation()
        try:
            result = r.projection(['grade'])
            assert False
        except UnexpectedCol:
            pass

    def test_add_invalid_row(self):
        """关于添加记录行的测试"""
        r = create_tmp_relation()
        try:
            r.add_row([1, 'Amy'])  # 缺少字段
            assert False
        except UnexpectedRow:
            pass
        try:
            r.add_row([1, 1, 1, 1])  # 多余字段
            assert False
        except UnexpectedRow:
            pass

    def test_init_add_valid_row(self):
        """正确添加了一行记录的情况"""
        r = create_tmp_relation()
        record = [4, 'Amy', 78]
        r.add_row(record)
        self.assertListEqual(
            record,
            r.switch_rows(lambda x: x.fields[0] == 4).rows[0].fields)


if __name__ == '__main__':
    unittest.main()
