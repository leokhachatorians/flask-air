import pprint

class DTable():
    def __init__(self, id_, name, columns):
        self.id_ = id_
        self.name = name
        self.columns = columns

        self._set_table_info()

    def _remove_column(self):
        pass

    def _add_column(self, name, type_):
        if name in self.table_info['column_names']:
            print('duplicate')
        else: print('unique')

    def _alter_column(self):
        pass

    def _set_table_info(self):
        self.table_info = {
                'table_name': self.name,
                'table_id': self.id_,
                'columns': [],
                'column_names': [],
        }
        for column in self.columns:
            self.table_info['columns'].append("{}".format(column))
            self.table_info['column_names'].append(column.column_name)

    def _list_table(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(self.table_info)
