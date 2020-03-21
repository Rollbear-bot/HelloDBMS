# -*- coding: utf-8 -*-
# @Time: 2020/3/17 10:38
# @Author: Rollbear
# @Filename: test_relation.py

import unittest

from entity.relation import *
from entity.exceptions import *
from entity.row import Row


# 不要修改这个文件的内容

def create_tmp_relation():
    """生成一个测试用关系对象"""
    result = Relation(['id', 'name', 'score'])
    result.add_row([1, 'John', 99])
    result.add_row([2, 'Sally', 98])
    result.add_row([3, 'Tom', 80])
    return result


def create_tmp_relations():
    """
    生成一组测试用关系对象
    :return: 四元组（社团关系，参加关系，学生关系，宿舍关系）
    """
    association, join, student, dormitory = Relation(["社团编号", "社团名", "学号"]), \
        Relation(["学号", "社团编号"]),\
        Relation(["学号", "姓名", "性别", "院系", "班级", "宿舍编号"]),\
        Relation(["宿舍编号", "房间号", "宿舍楼"])
    # 添加学生
    student.add_row([1, "张三", "男", "计算机学院", "3班", 1])
    student.add_row([2, "李四", "男", "计算机学院", "3班", 1])
    student.add_row([3, "王五", "男", "计算机学院", "4班", 2])
    student.add_row([4, "Tom", "男", "计算机学院", "4班", 2])
    student.add_row([5, "Jack", "男", "经管学院", "3班", 3])
    student.add_row([6, "John", "男", "经管学院", "3班", 4])
    student.add_row([7, "Sam", "男", "经管学院", "5班", 4])
    student.add_row([8, "Tom", "男", "经管学院", "4班", 4])
    # 添加社团
    association.add_row([1, "篮球社", 1])
    association.add_row([2, "足球社", 1])
    association.add_row([3, "动漫社", 6])
    # 添加参加关系
    join.add_row([1, 1])  # 张三参加篮球社
    join.add_row([1, 2])  # 张三参加足球社
    join.add_row([2, 1])  # 李四参加篮球社
    join.add_row([3, 1])  # 王五参加篮球社
    join.add_row([3, 2])  # 王五参加足球社
    join.add_row([6, 3])  # Jack参加动漫社
    # 添加宿舍
    dormitory.add_row([1, "322", "东十二"])
    dormitory.add_row([2, "323", "东十二"])
    dormitory.add_row([3, "222", "东十三"])
    dormitory.add_row([4, "222", "东十三"])
    return association, join, student, dormitory


class TestRelation(unittest.TestCase):
    """关系对象测试类"""

    def test_switch_one_row(self):
        """对行选取方法的测试"""
        r = create_tmp_relation()
        result = r.selection(lambda x: x.fields[1] == 'Tom')
        self.assertEqual(len(result.rows), 1)
        self.assertListEqual(result.cols, ['id', 'name', 'score'])
        self.assertListEqual(result.rows[0].fields, [3, 'Tom', 80])

    def test_switch_two_rows(self):
        """测试从关系中选取两行"""
        r = create_tmp_relation()
        result = r.selection(lambda x: x.fields[2] > 90)
        self.assertEqual(len(result.rows), 2)
        self.assertListEqual(result.cols, ['id', 'name', 'score'])
        self.assertListEqual(result.rows[0].fields, [1, 'John', 99])
        self.assertListEqual(result.rows[1].fields, [2, 'Sally', 98])

    def test_switch_None(self):
        """所有行不满足条件时"""
        r = create_tmp_relation()
        result = r.selection(lambda x: x.fields[2] > 100)
        self.assertEqual(len(result.rows), 0)
        self.assertTrue(result.is_empty())

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
            r.selection(lambda x: x.fields[0] == 4).rows[0].fields)


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
        self.assertTrue(result.rows[3].fields[0] == 5)

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


class TestDifference(unittest.TestCase):
    """差运算测试类"""

    def test_difference(self):
        """测试差运算（常规情况）"""
        r1 = create_tmp_relation()
        r2 = Relation(r1.cols.copy())
        r2.add_row([2, 'Sally', 98])
        r2.add_row([5, 'Jack', 60])
        result = r1 - r2
        self.assertListEqual(result.cols, r1.cols)
        self.assertListEqual(result.rows[1].fields, [3, 'Tom', 80])

    def test_invalid_relation_difference(self):
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

    def test_intersection_case_2(self):
        """交运算测试用例2"""
        association, join, student, dormitory = create_tmp_relations()
        r1 = student.natural_join(dormitory) \
            .selection(lambda x: x.fields[x.index('院系')] == '经管学院' and x.fields[x.index('班级')] == '3班') \
            .projection(['宿舍楼', '房间号'])
        r2 = student.natural_join(dormitory) \
            .selection(lambda x: x.fields[x.index('院系')] == '经管学院' and x.fields[x.index('班级')] == '5班') \
            .projection(['宿舍楼', '房间号'])
        result = r1.intersection(r2)
        self.assertListEqual(result.rows[0].fields, ['东十三', '222'])

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
        self.assertTrue(result.is_empty())
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
            result.selection(lambda x: x.fields[3] == 'A').rows[0].fields,
            [1, 'John', 99, 'A'])
        self.assertListEqual(
            result.selection(lambda x: x.fields[0] == 2).rows[0].fields,
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

    def test_div_case_3(self):
        """除法/混合运算测试用例3"""
        association, join, student, dormitory = create_tmp_relations()
        # 找出所有参加了“王五”参加的所有社团的学生姓名
        r1 = student.natural_join(join).projection(['姓名', '社团编号'])
        r2 = student.natural_join(join).selection(
            lambda x: x.fields[x.index('姓名')] == '王五').projection(['社团编号'])
        result = r1 / r2
        for row in result.rows:
            self.assertTrue(row.fields in [['张三'], ['王五']])

    def test_div_case_4(self):
        """除法/混合运算测试用例4"""
        association, join, student, dormitory = create_tmp_relations()
        r1 = student.projection(['姓名', '院系', '班级', '宿舍编号'])
        r2 = student.natural_join(association)\
            .selection(lambda x: x.fields[x.index('社团名')] == '动漫社')\
            .projection(['宿舍编号'])
        # 找出动漫社负责人的舍友的姓名、院系、班级
        result = (r1 / r2) - student.natural_join(association)\
            .selection(lambda x: x.fields[x.index('社团名')] == '动漫社')\
            .projection(['姓名', '院系', '班级'])
        for row in result.rows:
            self.assertTrue(row.fields[0] in ['Tom', 'Sam'])


class TestRow(unittest.TestCase):
    """记录行测试类"""
    def test_eq(self):
        col_names = ['a', 'b', 'c']
        r1 = Row([1, 2, 3], col_names)
        r2 = Row([2, 1, 3], col_names)
        self.assertFalse(r1 == r2)
        r3 = Row([1, 2, 3], col_names)
        self.assertTrue(r1 == r3)


if __name__ == '__main__':
    unittest.main()
