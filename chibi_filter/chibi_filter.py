# -*- coding: utf-8 -*-
import functools
from chibi_filter.serializer import Q_serializer
from chibi_filter.descriptor import Descriptor
from chibi_filter.q import Q
import operator
import chibi_donkey as donkey
from chibi_filter.exceptions import Invalid_filter, Filter_not_exits
from copy import copy
from chibi.atlas import Chibi_atlas


class Chibi_filter_container:
    def __init__( self, filters ):
        self.filters = filters


class Meta_base:
    def __init__( self ):
        self._filters = Chibi_atlas()
        self._model = object


class Chibi_filter_meta( type ):
    def __new__( cls, cls_name, bases, cls_dict ):
        fields = []
        more_filters = []
        for k, v in cls_dict.items():
            if isinstance( v, Descriptor ):
                fields.append( k )
                cls_dict[ k ].name = k
            elif isinstance( v, Chibi_filter_container ):
                more_filters.append( ( k, v ) )

        attr_meta = cls_dict.pop( 'Meta', None )
        cls_obj = super().__new__( cls, cls_name, bases, cls_dict )

        if attr_meta is None:
            if hasattr( cls_obj, '_meta' ):
                attr_meta = cls_obj._meta
            else:
                attr_meta = Meta_base()
            cls_obj.Meta = attr_meta
        else:
            cls_obj.Meta = attr_meta
        meta_base = getattr( cls_obj, 'Meta', None )
        cls_obj._meta = Meta_base()
        cls_obj._meta.__dict__.update( meta_base.__dict__.copy() )
        if hasattr( attr_meta, 'model' ):
            cls_obj._meta.model = attr_meta.model
            cls_obj._meta._model = attr_meta.model
        attr_meta = cls_obj._meta

        if hasattr( attr_meta, '_filters' ):
            attr_meta._filters = {}
        #attr_meta._filters.update( meta_base._filters )
        attr_meta._filters.update( {
            name: cls_dict[ name ]
            for name in fields
        } )

        for name, chibi_filter in more_filters:
            inner_filters = chibi_filter.filters
            attr_meta._filters[ name ] = inner_filters

        return cls_obj


class Chibi_filter( metaclass=Chibi_filter_meta ):
    """
    Contenedor de descriptores para los filtros
    """
    class Meta:
        pass

    def __init__( self, data=None, queryset=None, *args, **kargs ):
        self.data = data
        self.queryset = queryset
        if self.data:
            self.serialize_data()
            self.process_q = self.evaluate_q()
        else:
            self.process_q = None

    def is_valid( self ):
        return True

    @property
    def qs( self ):
        return self.doing_query()

    def serialize_data( self ):
        serializer = Q_serializer( data=self.data )
        self.q = serializer.parse()

    def evaluate_q( self, q=None ):
        """
        evalua el objeto Q de chibi_filter y los tranforma en los
        objetos Q de los descriptores
        """
        if q is None:
            q = self.q

        result = self.process_q_node( q )
        return result

    def doing_query( self ):
        """
        hace el query, solo funciona para objetos Search de elasticsearch_dsl
        """
        if self.process_q:
            return self.queryset.query( self.process_q )
        return self.queryset

    def descriptor( self ):
        """
        regresa el descriptor para los filtros nested
        """
        return Chibi_filter_container( self._meta._filters )

    def nested( self, prefix ):
        filters = {}
        for name, filter in self._meta._filters.items():
            filter_copy = copy( filter )
            filter_copy.transform_to_nested( prefix )
            filters[name] = filter_copy
        return Chibi_filter_container( filters )

    @classmethod
    def process_q_node( cls, q ):
        """
        Evalua los objetos Q de tipo Nodo
        """
        if not isinstance( q, Q ):
            childrens = []
            for q_child in q.children:
                q_proceser = cls.process_q_node( q_child )
                childrens.append( q_proceser )
            if q.op == Q.AND:
                result = functools.reduce( operator.and_, childrens )
            elif q.op == Q.OR:
                result = functools.reduce( operator.or_, childrens )
            return result
        else:
            return cls.process_q_leaf( q )

    @classmethod
    def process_q_leaf( cls, q ):
        """
        Evalua los objetos Q de tipo Leaf
        """
        lookup = q.lookup
        for key, value in lookup.items():
            #field_name = donkey.key( *donkey.partion( key )[:-1] )
            field_name = donkey.init( key )
            filter_field = cls.get_filter_by_donkey( field_name )
            if filter_field is None:
                raise Invalid_filter( field_name )
            if isinstance( filter_field, dict ):
                raise NotImplementedError(
                    f"la extracion de filtro obtubu un "
                    f"dicionario {filter_field!r}" )
            convert_q = filter_field.convert_q( q )
        return convert_q

    @classmethod
    def get_filter_by_donkey( cls, key ):
        """
        Obtiene el filtro usando el formato de donkey
        """
        filters = cls._meta._filters
        try:
            return donkey.get( key, filters )
        except KeyError as e:
            raise Filter_not_exits( str( e ) ) from e
