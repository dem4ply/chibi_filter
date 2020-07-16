import copy


class Node:
    """
    Base de los objetos Q
    la estructura es un Arbol binario
    """
    AND = 'AND'
    OR = 'OR'

    NODE_CLASS = None

    def __init__( self, *args, **kw ):
        self.negate = False
        self.children = []
        self.op = self.AND

        if self.NODE_CLASS is None:
            self._node_class = self.__class__
        else:
            self._node_class = self.NODE_CLASS

    def __repr__( self ):
        if self.negate:
            result = (
                f"<class not {type( self )}( op={self.op}, "
                f"children={self.children} )>"
            )
        else:
            result = (
                f"<class {type( self )}( op={self.op}, "
                f"children={self.children} )>"
            )
        return result

    def __copy__( self ):
        return copy.deepcopy( self )

    def __deepcopy__( self, extra_shit ):
        new_node = self.__class__()
        new_node.negate = self.negate
        new_node.op = self.op
        for child in self.children:
            new_node.append( child )
        return new_node

    def append( self, other ):
        self.children.append( other )

    def __and__( self, other ):
        node = self._node_class()
        node.append( self )
        node.append( other )
        return node

    def __or__( self, other ):
        node = self._node_class()
        node.op = Node.OR
        node.append( self )
        node.append( other )
        return node

    def __invert__( self ):
        new_node = copy.deepcopy( self )
        new_node.negate = not self.negate
        return new_node

    def to_dict( self ):
        result = {
            'op': self.op,
            'negate': self.negate,
            'childrens': [ child.to_dict() for child in self.children ]
        }
        return result
