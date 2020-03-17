# -*- coding: utf-8 -*-
# @Time: 2020/3/17 10:38
# @Author: Rollbear
# @Filename: test_relation.py

import unittest

from entity.relation import Relation2, Row
from entity.exceptions import *


def create_tmp_relation():
    result = Relation2()
    result.add_col('id', [])
    result.add_col('name', [])
    result.add_col('score', [])
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


if __name__ == '__main__':
    unittest.main()
