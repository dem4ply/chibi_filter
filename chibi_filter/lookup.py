class Lookup:
    def __init__( self, field, lookup, value, nested_path=None ):
        self.field = field
        self.lookup = lookup
        self.value = value
        self.nested_path = nested_path

    def build( self, value=None ):
        """
        Contrulle el objeto Q segun el descriptor
        se tiene que definir en cada clase hijo
        """
        raise NotImplementedError(
            ( "this is the class base for filters lookup" ) )

    def transform_to_nested( self, q ):
        raise NotImplementedError(
            ( "this is the class base for filters lookup" ) )
