# -*- coding: utf-8 -*-
# @Time: 2020/3/17 10:38
# @Author: Rollbear
# @Filename: test_relation.py

import unittest

from entity.relation import *
from entity.exceptions import *
from entity.row import Row


def create_tmp_relation():
    """生成一个测试用关系对象"""
    result = Relation(['id', 'name', 'score'])
    result.add_row([1, 'John', 99])
    result.add_row([2, 'Sally', 98])
    result.add_row([3, 'Tom', 80])
    return result


class TestRelation(unittest.TestCase):
    """关系对象测试类"""

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
        """所有行不满足条件时"""
        r = create_tmp_relation()
        result = r.switch_rows(lambda x: x.fields[2] > 100)
        self.assertEqual(len(result.rows), 0)
        self.assertFalse(not result.is_empty())

    def test_relation_standardizing(self):
        """测试关系的重构方法"""
        r = create_tmp_relation()
        pattern = Relation(['id', 'score', 'name'])
        r.standardizing(pattern)
        self.assertListEqual(r.cols, ['id', 'score', 'name'])
        self.assertEqual(r.rows[0].fields[2], 'John')


class TestProjection(unittest.TestCase):
    """投影运算测试类
    """
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

    def test_projection_same_rows(self):
        """投影中有相同行时"""
        r = create_tmp_relation()
        r.add_row([4, 'Jack', 99])
        result = r.projection(['score'])
        self.assertEqual(len(result.rows), 3)

    def test_invalid_col_projection(self):
        """测试投影出空集的情况"""
        r = create_tmp_relation()
        try:
            result = r.projection(['grade'])
            assert False
        except UnexpectedCol:
            pass


class TestAddRow(unittest.TestCase):
    """行追加测试类"""

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


class TestUnion(unittest.TestCase):
    """并运算测试类"""

    def test_union(self):
        """并运算测试（常规情况）"""
        r1 = create_tmp_relation()
        r2 = Relation(r1.cols.copy())
        r2.add_row([2, 'Sally', 98])
        r2.add_row([5, 'Jack', 60])
        result = r1 + r2
        self.assertEqual(len(result.rows), 4)
        self.assertFalse(not result.rows[3].fields[0] == 5)

    def test_invalid_relation_union(self):
        """对不合法的关系执行并运算"""
        r1 = create_tmp_relation()
        r2 = Relation(['id', 'name'])
        r2.add_row([5, 'Jack'])
        try:
            # 此处应当抛出异常
            r1 + r2
            assert False
        except UnexpectedRelation:
            pass


class TestSub(unittest.TestCase):
    """差运算测试类"""

    def test_sub(self):
        """测试差运算（常规情况）"""
        r1 = create_tmp_relation()
        r2 = Relation(r1.cols.copy())
        r2.add_row([2, 'Sally', 98])
        r2.add_row([5, 'Jack', 60])
        result = r1 - r2
        self.assertListEqual(result.cols, r1.cols)
        self.assertListEqual(result.rows[1].fields, [3, 'Tom', 80])

    def test_invalid_relation_sub(self):
        """非法关系下的差运算"""
        r1 = create_tmp_relation()
        r2 = Relation(['id', 'name'])
        r2.add_row([2, 'Sally'])
        try:
            tmp = r1 - r2
            assert False
        except UnexpectedRelation:
            pass


class TestCartesianProduct(unittest.TestCase):
    """笛卡儿积运算测试"""

    def test_cartesian_product(self):
        """测试笛卡尔积（常规情况）"""
        r1 = create_tmp_relation()
        r2 = Relation(['id', 'class'])
        r2.add_row(['01', 'A'])
        r2.add_row(['02', 'B'])
        result = r1 * r2
        self.assertEqual(len(result.rows), len(r1.rows) * len(r2.rows))


class TestIntersection(unittest.TestCase):
    """交运算测试类"""

    def test_intersection(self):
        """测试交运算（常规情况）"""
        r1 = create_tmp_relation()
        r2 = Relation(r1.cols.copy())
        r2.add_row([2, 'Sally', 98])
        r2.add_row([4, 'Jack', 98])
        result = r1.intersection(r2)
        self.assertEqual(len(result.cols), 3)
        self.assertEqual(len(result.rows), 1)
        self.assertListEqual(result.rows[0].fields, [2, 'Sally', 98])

    def test_invalid_relation_intersection(self):
        """非法关系的交运算"""
        r1 = create_tmp_relation()
        r2 = Relation(['id', 'name'])
        r2.add_row([1, 'John'])
        try:
            tmp = r1.intersection(r2)
            assert False
        except UnexpectedRelation:
            pass

    def test_empty_result_intersection(self):
        """无交集时"""
        r1 = create_tmp_relation()
        r2 = Relation(r1.cols.copy())
        r2.add_row([5, 'John', 99])
        result = r1.intersection(r2)
        self.assertFalse(not result.is_empty())
        self.assertEqual(len(result.rows), 0)
        self.assertListEqual(result.cols, r1.cols)


class TestNaturalJoin(unittest.TestCase):
    """自然连接运算测试类"""

    def test_natural_join(self):
        """自然连接（常规情况）"""
        r1 = create_tmp_relation()
        r2 = Relation(['id', 'class'])
        r2.add_row([1, 'A'])
        r2.add_row([2, 'B'])
        r2.add_row([5, 'B'])
        result = r1.natural_join(r2)
        self.assertEqual(len(result.rows), 2)
        self.assertListEqual(
            result.switch_rows(lambda x: x.fields[3] == 'A').rows[0].fields,
            [1, 'John', 99, 'A'])
        self.assertListEqual(
            result.switch_rows(lambda x: x.fields[0] == 2).rows[0].fields,
            [2, 'Sally', 98, 'B'])

    def test_natural_join_unexpected_relation(self):
        """使用非法的关系进行自然连接"""
        r1 = create_tmp_relation()
        r2 = Relation(['s_id', 's_name'])
        try:
            tmp = r1.natural_join(r2)
            assert False
        except UnexpectedRelation:
            pass


class TestDiv(unittest.TestCase):
    """除法运算测试类"""

    def test_div_case_1(self):
        """测试除法运算（常规情况）"""
        r1 = create_tmp_relation()
        r1.add_row([3, 'Tom', 98])
        r2 = Relation(['score'])
        r2.add_row([98])
        r2.add_row([80])
        result = r1 / r2
        self.assertListEqual(result.cols, ['id', 'name'])
        self.assertEqual(len(result.rows), 1)
        self.assertListEqual(result.rows[0].fields, [3, 'Tom'])

    def test_div_case_2(self):
        """除法运算测试用例2"""
        r1 = Relation(['name', 'course', 'score'])
        r1.add_row(['ZJ', 'Physic', 93])
        r1.add_row(['WH', 'Math', 86])
        r1.add_row(['ZJ', 'Math', 93])
        r1.add_row(['ZJ', 'Physic', 92])
        r2 = Relation(['course'])
        r2.add_row(['Math'])
        r2.add_row(['Physic'])
        result = r1 / r2
        self.assertListEqual(result.rows[0].fields, ['ZJ', 93])


class TestRow(unittest.TestCase):
    """记录行测试类"""
    def test_eq(self):
        col_names = ['a', 'b', 'c']
        r1 = Row([1, 2, 3], col_names)
        r2 = Row([2, 1, 3], col_names)
        self.assertFalse(r1 == r2)
        r3 = Row([1, 2, 3], col_names)
        self.assertFalse(not r1 == r3)


if __name__ == '__main__':
    unittest.main()
