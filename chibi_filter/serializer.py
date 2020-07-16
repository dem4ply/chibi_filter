from chibi_filter.q import Q


class Q_serializer:
    """
    Serializa los objetos Q de mad_filter

    Arguments
    =========
    instance: instancia Q de mad_filter
    data: dicionario que se tranformara en un objeto Q
    """

    def __init__( self, instance=None, data=None ):
        self.instance = instance
        self.data = data

    def parse( self ):
        """
        regresa el objeto Q si se mando data o regresa el dicionario
        de la instancia del objeto Q
        """
        if self.instance is not None:
            return self._parse_instance()
        elif self.data is not None:
            return self._parse_data()
        else:
            raise ValueError( "need instance of Q object or data for tranform" )

    def _parse_instance( self ):
        return self.instance.to_dict()

    def _parse_data( self ):
        return self._parse_q( self.data )

    def _parse_q( self, data ):
        op = data[ 'op' ]
        negate = data[ 'negate' ]
        children = []
        try:
            for child in data[ 'childrens' ]:
                children.append( self._parse_q( child ) )
            if op == 'AND':
                q = children[0] & children[1]
            else:
                q = children[0] | children[1]
        except KeyError:
            q = Q( **data[ 'lookup' ] )

        if negate:
            q = ~q
        return q
