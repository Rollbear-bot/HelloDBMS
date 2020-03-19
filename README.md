# A simple Library for Relation Algebra
+ What is Relation Algebra?
  + Relational algebra is a kind of abstract query language. It uses the operation of relation to express the query, as a mathematical tool to study the relation data language. The operation object of relational algebra is relation, and the operation result is relation.

+ Why the repo?
  + For skill learning:books:, experimenting:wrench: after class.
  + More for fun:happy:!



## Features:fire:

### Classic relation operations, 基本关系运算

1. **Selection**, 选择运算

   + By calling the `selection(lambda)` method.

   + Define a `lambda` to choose the rows you want, and use `Row.index()` to locate a field, just like the below.

     ```python
     relation = r.selection(
         lambda row: row[row.index('YOUR_FIELD_NAME')] 
         	== YOUR_FIELD_VALUE
     )
     ```

2. **Projection**, 投影运算

   + By providing a field list to `projection` method.

   + Choose the columns you need.

     ```python
     relation = r.projection(['id', 'name'])
     ```

3. **Extended Cartesian Product**, 广义笛卡尔积

   + By using the  `*` operator.

   + The `__mul__` method return a Cartesian Product *(object of Relation)* from two relation operands.

   + Quick and easy, just like the follow.

     ```python
     relation = r1 * r2
     ```

4. **Union**, 并运算

   + By using the `+` operator.

   + The `__add__` method return a Union from two relation operands.

     ```python
     relation = r1 + r2
     ```

5. **Difference**, 差运算

   + By using the `-` operator.

   + The `__sub__` method return Difference from two relation operands.

     ```python
     relation = r1 - r2
     ```



### Specific relation operations, 特殊关系运算

1. **Intersection**, 交运算
   
   + The `intersection` method operate the *self* and the *other* object and return a intersection *(object of Relation)*.
   
     ```python
     relation = r1.intersection(r2)
     ```

2. **Natural Join**, 自然连接

   + The "Natural Join" picks the some-named fields and make special connection between two relation objects.

     ```python
     relation = r1.natural_join(r2)
     ```

3. **Division**, 除运算

   + The most magical operation in all over.

   + By using the operator `/` .

     ```python
     relation = r1 / r2
     ```

     

## Getting Start:rocket:

+ Clone this repo.
+ Or, download the zip package.



### Then 

1. Create a python file in your project directory, or open a Python Console.

2. Import necessary modules.

   ```python
   >>> from entity.relation import Relation
   ```

3. Create an instance of Relation, setting its  fields to make init.

   ```python
   >>> relation = Relation(['id', 'name', 'score'])  # Just like this!
   ```

4. Append rows, by calling the `add_row()` method.

   ```python
   >>> relation.add_row([1, 'John', 98])  # id: 1, name: John, score: 98
   >>> relation.add_row([2, 'Tom', 80])  # id: 2, name: Tom, score: 80
   ```

5. Try your expressions!

   ```python
   >>> print(relation)  # Print the relation object your just created.
       id       name     score   
       1        John       98    
       2        Tom        80    
   ```

   + Define a `lambda` to make a selection.

     ```python
     >>> # Select the rows whose 'id' == 2.
     >>> print(relation.selection(
     >>>		lambda x: x.fields[x.index('id')] == 2
     >>> ))
         id       name     score   
         2        Tom        80    
     ```

     ```python
     >>> print(relation.selection(
     >>> 	lambda x: x.fields[x.index('id')] == 2 
     >>> 	or x.fields[x.index('score')] == 98
     >>> ))
         id       name     score   
         1        John       98    
         2        Tom        80    
     ```

   + Push your fields in, and get projection return.

     ```python
     >>> print(relation.projection(['name', 'score']))
        name     score   
        John       98    
        Tom        80    
     ```




## ToDo:wrench:

+ Some bugs in `__mul__`, when the method operate the relations with same-name fields.





