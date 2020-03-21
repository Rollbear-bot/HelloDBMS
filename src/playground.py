# -*- coding: utf-8 -*-
# @Time: 2020/3/17 14:05
# @Author: Rollbear
# @Filename: playground.py

from entity.relation import Relation


def main():
    # 1.Define your relation objects here.
    student_r = Relation(['s_id', 's_name', 'class'])   # s_id  s_name  class
    student_r.add_row([1, 'John', 'Class 3'])           # 1     John    Class 3
    student_r.add_row([2, 'Tom', 'Class 4'])            # 2     Tom     Class 4

    # 2.Write your expressions here.
    result = student_r.projection(['s_name'])

    # 3.Print the result here
    result.show()

    # Then run the script!


if __name__ == '__main__':
    main()
