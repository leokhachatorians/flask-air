from dtable import DTable
from dt_column import DTColumn

# id, name, type, sequence_number
col_1 = DTColumn(1, "first", "Text")
col_2 = DTColumn(2, "second", "Text")
col_3 = DTColumn(3, "third", "Text")
col_4 = DTColumn(4, "fourth", "Text")
columns = [col_1, col_2, col_3, col_4]

table1 = DTable(1, "Unsorted", columns)
print(table1._list_table())

#columns.sort(key=lambda x: x.sequence_number)

table2 = DTable(2, "Sorted", columns)
print(table2._list_table())
