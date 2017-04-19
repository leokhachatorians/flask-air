class DTDataEngine():
    """Empty Abstract Base
    """
    pass

class DTDataEngineJSON(DTDataEngine):
    pass

class DTDataEngineSQL(DTDataEngine):
    def __init__(self):
        pass

    def set_schema(self, table_name, table):
        pass
