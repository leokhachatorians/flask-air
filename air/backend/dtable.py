import pprint
from .dt_column import DTColumn
from .excp.duplicate_column import DuplicateColumnException

class DTable():
    def __init__(self, id_, name, columns):
        self.id_ = id_
        self.name = name
        self.columns = columns

        self._set_table_info()

    def _remove_column(self):
        pass

    def _add_column(self, name, type_):
        try:
            self.table_info['columns'][name]
            raise DuplicateColumnException(
                self.id_, self.table_info['columns'][name].column_id, name)
        except KeyError:
            self.table_info['modifications']['new']['name'] = name
            self.table_info['modifications']['new']['type'] = type_
            print(self.table_info)

    def _alter_column(self):
        pass

    def _set_table_info(self):
        self.table_info = {
            'table_name': self.name,
            'table_id': self.id_,
            'columns': {},
            'modifications': {
                'new': {
                    'name': None,
                    'type': None,
                },
                'altered': {
                    'name': None,
                    'type': None,
                },
                'deleted': None,
            }
        }
        for column in self.columns:
            self.table_info['columns'][column.column_name] = column

    def _list_table(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(self.table_info)
