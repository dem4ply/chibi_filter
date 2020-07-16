from unittest import TestCase
from copy import copy
from chibi_filter.descriptor import Descriptor, Numeric
from chibi_filter.exceptions import Lookup_invalid


class Test_descriptor( TestCase ):
    def test_evaluate_lookup( self ):
        field = Descriptor()
        with self.assertRaises( Lookup_invalid ):
            field.evaluate_lookup( 'eq' )

    def test_get_lookup_class( self ):
        field = Descriptor()
        with self.assertRaises( NotImplementedError ):
            field.get_lookup_class( 'some_field', 'eq', 'nothign' )

    def test_copy_is_not_the_same_instance( self ):
        field = Descriptor()
        field_copy = copy( field )
        self.assertIsNot( field, field_copy )

    def test_copy_have_the_same_name( self ):
        field = Descriptor()
        field_copy = copy( field )
        self.assertEqual(field.name, field_copy.name)

    def test_copy_is_the_same_insatance( self ):
        field = Descriptor()
        field_copy = copy( field )
        self.assertIsInstance( field_copy, Descriptor )

    def test_tranform_to_nested_have_prefix( self ):
        field = Descriptor()
        field.transform_to_nested( 'field' )
        self.assertEqual( field.nested_name, 'field' )

    def test_default_is_not_nested( self ):
        field = Descriptor()
        self.assertFalse( field.is_in_nested )


class Test_numeric( TestCase ):
    def test_evaluate_lookup( self ):
        field = Numeric()
        lookups = [ 'eq', 'gt', 'gte', 'lt', 'lte' ]
        for lookup in lookups:
            self.assertTrue( field.evaluate_lookup( lookup ) )

    def test_copy_is_the_same_insatance( self ):
        field = Numeric()
        field_copy = copy( field )
        self.assertIsInstance( field_copy, Numeric )
