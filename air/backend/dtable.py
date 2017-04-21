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
            self.info['columns'][name]
            return False
            #raise DuplicateColumn(
            #    self.id_, self.table_info['columns'][name].column_id, name)
        except KeyError:
            self.info['modifications']['new']['name'] = name
            self.info['modifications']['new']['type'] = type_
            return True

    def _alter_column(self, form, request):
        try:
            self.info['modifications']['altered']['name'] = form.column_name.data
            self.info['modifications']['altered']['type'] = form.types.data
            self.info['modifications']['altered']['id'] = request.form.getlist('col_to_alter')[0]
            return True
        except KeyError:
            return False

    def _remove_column(self, request):
        try:
            self.info['modifications']['deleted']['id'] = request.form.getlist('to_delete')[0]
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
                'new': {
                    'name': None,
                    'type': None,
                },
                'altered': {
                    'name': None,
                    'type': None,
                },
                'deleted': {
                    'id': None,
                },
            }
        }
        for column in self.columns:
            self.info['columns'][column.column_name] = column

    def _list_table(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(self.info)
