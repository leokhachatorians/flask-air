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

    def add_column(self, form):
        name = form.add_column_name.data
        type_ = form.types.data
        try:
            self.info['columns'][name]
            return False
            #raise DuplicateColumn(
            #    self.id_, self.table_info['columns'][name].column_id, name)
        except KeyError:
            self.info['modifications']['name'] = name
            self.info['modifications']['type'] = type_
            return True

    def alter_column(self, form):
        try:
            self.info['columns'][form.old_column_name.data]
            self.info['modifications']['name'] = form.edit_column_name.data
            self.info['modifications']['type'] = form.types.data
            self.info['modifications']['id'] = form.column_id.data
            return True
        except KeyError:
            return False

    def remove_column(self, form):
        try:
            self.info['columns'][form.delete_column_name.data]
            self.info['modifications']['id'] = form.delete_column_id.data
            return True
        except KeyError:
            return False

    def _set_table_info(self):
        """Sets up the internal dictionary to be consumed

        The 'info' dictionary is essentially the vehicle used to
        transport the information held by the DTable to 'DT Schema Store'.
        It contains basic information about what table to operate on, as well
        as what columns need to be altered, deleted, or created.
        """

        self.info = {
            'table_name': self.name,
            'table_id': self.id_,
            'columns': {},
            'modifications': {
                'name': None,
                'type': None,
                'id': None,
            }
        }
        for column in self.columns:
            self.info['columns'][column.column_name] = column

    def _list_table(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(self.info)
