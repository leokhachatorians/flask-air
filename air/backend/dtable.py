import pprint
from .dt_column import DTColumn
from .excp.column_exceptions import DuplicateColumn

class DTable():
    """Container for a users table

    Sole purpose of the DTable class is to be a bridge between the database and
    the user. Whenever the user wishes to modify their table in any matter, it
    first is modified here. The DTable will then be consumed by the 'DT Schema Store'
    which is in charge of actually modifying the meta-schema of the table in the
    actual database.
    """
    def __init__(self, id_, name, columns):
        self.id_ = id_
        self.name = name
        self.columns = columns

        self._set_table_info()

    def _add_column(self, name, type_):
        try:
            self.table_info['columns'][name]
            return "Column already exists"
            #raise DuplicateColumn(
            #    self.id_, self.table_info['columns'][name].column_id, name)
        except KeyError:
            self.table_info['modifications']['new']['name'] = name
            self.table_info['modifications']['new']['type'] = type_
            return True

    def _alter_column(self, name, type_):
        try:
            self.table_info['modifications']['altered']['name'] = name
            self.table_info['modifications']['altered']['type'] = type_
        except KeyError:
            return False

    def _remove_column(self, name):
        try:
            self.table_info['modifications']['deleted']['name'] = name
        except KeyError:
            return False

    def _set_table_info(self):
        """Sets up the internal dictionary to be consumed

        The table_info dictionary is essentially the vehicle used to
        transport the information held by the DTable to 'DT Schema Store'.
        It contains basic information about what table to operate on, as well
        as what columns need to be altered, deleted, or created.
        """

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
                'deleted': {
                    'name': None,
                },
            }
        }
        for column in self.columns:
            self.table_info['columns'][column.column_name] = column

    def _list_table(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(self.table_info)
