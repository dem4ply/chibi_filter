from chibi_filter.utils import Node


class Q_node( Node ):
    """
    Objeto Q de tipo Nodo
    """
    pass


class Q_leaf( Node ):
    """
    Hoja de los arboles de los objetos Q
    """
    NODE_CLASS = Q_node

    def __init__( self, *args, **kw ):
        super().__init__( *args, **kw )
        self.lookup = kw

    def __deepcopy__( self, other ):
        new_node = self.__class__( **self.lookup )
        new_node.negate = self.negate
        new_node.op = self.op
        return new_node

    def to_dict( self ):
        result = {
            'op': self.op,
            'negate': self.negate,
            'lookup': self.lookup
        }
        return result


Q = Q_leaf
