# -*- coding: utf-8 -*-
# @Time: 2020/3/16 19:11
# @Author: Rollbear
# @Filename: unit_tests.py

import unittest
'''
from entity.exceptions import UnexpectedRow, UnexpectedCol, RowNoFound
from entity.relation import Relation


def creat_a_tmp_relation():
    relation = Relation()
    # 添加测试用的列和行
    relation.add_col('student_id', [1, 2, 3])
    relation.add_col('student_name', ['John', 'Sally', 'Tom'])
    relation.add_col('score', [100, 59, 90])
    return relation


class TestRelation(unittest.TestCase):

    def test_add_row_and_col(self):
        """关于添加记录行的测试"""
        relation = creat_a_tmp_relation()
        lt = [4, 'Amy', 89]
        relation.add_row(lt)
        # cols中相应位置的内容应该和刚加入的列表相同
        for index in range(len(lt)):
            self.assertEqual(lt[index], relation.cols[index].rows[3])

    def test_unexpected_col(self):
        """尝试添加不正确的属性列时能否正确抛出异常"""
        relation = creat_a_tmp_relation()
        try:
            relation.add_col('weight', [120, 150])
            assert False
        except UnexpectedCol:
            pass

    def test_unexpected_row(self):
        """尝试添加不正确的行时能否正确地抛出异常"""
        relation = creat_a_tmp_relation()
        try:
            relation.add_row([4, 'Amy'])
            assert False
        except UnexpectedRow:
            pass

    def test_get_row(self):
        """测试获取记录"""
        row = creat_a_tmp_relation().get_row(index=1)
        self.assertListEqual(row, [2, 'Sally', 59])

    def test_get_invalid_row(self):
        """尝试从空表中获取记录或获取不存在的记录行"""
        try:
            Relation().get_row(1)
            assert False
        except RowNoFound:
            pass
        try:
            creat_a_tmp_relation().get_row(3)
            assert False
        except RowNoFound:
            pass


if __name__ == '__main__':
    unittest.main()
'''