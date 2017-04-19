import pprint

class DTable():
    def __init__(self, id_, name, columns):
        self.id_ = id_
        self.name = name
        self.columns = columns

    def _remove_column(self):
        pass

    def _add_column(self, name, type_):
        pass

    def _alter_column(self):
        pass

    def _list_table(self):
        pp = pprint.PrettyPrinter(indent=4)
        table_info = {
                'table_name': self.name,
                'table_id': self.id_,
                'columns': []
        }
        for column in self.columns:
            table_info['columns'].append("{}".format(column))

        return pp.pformat(table_info)
