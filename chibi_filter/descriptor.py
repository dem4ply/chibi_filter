from chibi_filter.exceptions import Lookup_invalid
#from mad_filter import donkey

import chibi_donkey as donkey


class Descriptor:
    """
    Describe un filtro
    """
    lookup = []
    default = None

    def __init__( self, name=None, default=None ):
        self.name = name
        if default is not None:
            self.default = default
        self._is_in_nested = False
        self._nested_name = None

    def __copy__(self):
        return type( self )( name=self.name, default=self.default )

    def __get__( self, instance, cls ):
        return instance.__dict__.get( self.name, self.default )

    def __set__( self, instance, value ):
        instance.__dict__[self.name] = value

    def __repr__( self ):
        return f"descriptor.{type( self ).__name__}"

    def transform_to_nested( self, prefix ):
        self.is_in_nested = True
        self.nested_name = prefix

    @property
    def is_in_nested( self ):
        """
        si es parte de un filtro de nested
        """
        return self._is_in_nested

    @is_in_nested.setter
    def is_in_nested( self, value ):
        self._is_in_nested = value

    @property
    def nested_name( self ):
        """
        nombre de prefijo de la llave para el nested
        """
        return self._nested_name

    @nested_name.setter
    def nested_name(self, value):
        self._nested_name = value

    def evaluate_lookup( self, lookup ):
        """
        evalua si el lookup es parte del descriptor
        """
        if lookup not in self.lookup:
            raise Lookup_invalid()
        return True

    def get_lookup_class( self, key, lookup, value, nested_path=None ):
        """
        regresa la instancia para los lookups de cada clase
        se tiene que definir en cada descriptor
        """
        raise NotImplementedError

    def convert_q( self, q ):
        """
        Convierte el objeto Q de mad_filter al objeto Q que pertenece el
        descriptor
        """
        lookups = q.lookup
        list_q = []
        for key, value in lookups.items():
            field = donkey.init( key )
            lookup = donkey.last( key )
            if self.is_in_nested:
                lookup_class = self.get_lookup_class(
                    field, lookup, value, self.nested_name )
            else:
                lookup_class = self.get_lookup_class( field, lookup, value )
            current_q = lookup_class.build()
            list_q.append( current_q )
        result = list_q.pop( 0 )
        if len( list_q ) > 0:
            for q_new in list_q:
                result = result & q_new
        return result


class Any( Descriptor ):
    pass


class Numeric( Descriptor ):
    lookup = [ 'eq', 'gt', 'gte', 'lt', 'lte' ]


class Datetime( Descriptor ):
    lookup = [ 'eq', 'gt', 'gte', 'lt', 'lte' ]


class String( Descriptor ):
    lookup = [ 'eq', 'in', 'contain', 'fullsearch', 'regex' ]


class Boolean( Descriptor ):
    lookup = [ 'eq' ]
