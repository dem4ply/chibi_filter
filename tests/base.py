from unittest import TestCase
from chibi_filter import Chibi_filter
from chibi_filter import descriptor
from unittest.mock import Mock


class Filter_empty( Chibi_filter ):
    pass


class Filter_descriptor( Chibi_filter ):
    test_descriptor = descriptor.Descriptor()
    test_any = descriptor.Any()


class Filter_model_meta( Chibi_filter ):
    class Meta:
        model = Mock()


class Filter_descriptor_and_meta( Chibi_filter ):
    test_descriptor = descriptor.Descriptor()
    test_any = descriptor.Any()

    class Meta:
        model = Mock()


class Filter_for_inner( Chibi_filter ):
    test_descriptor = descriptor.Descriptor()
    test_any = descriptor.Any()


class Filter_with_inner( Chibi_filter ):
    test_filter_inner = Filter_for_inner().descriptor()


class Filter_with_nested( Chibi_filter ):
    test_filter_nested = Filter_for_inner().nested('test_filter_nested')


class Test_mad_filter( TestCase ):

    def test_instanciate_filter_empty( self ):
        inst_filter = Filter_empty()

        self.assertEqual( inst_filter._meta._filters, {} )
        self.assertEqual( inst_filter._meta._model, object )

        return inst_filter

    def test_instanciate_filter_descriptor( self ):
        inst_filter = Filter_descriptor()

        self.assertEqual( inst_filter._meta._model, object )

        self.assertIsInstance(
            inst_filter._meta._filters[ 'test_descriptor' ],
            descriptor.Descriptor )
        self.assertIsInstance(
            inst_filter._meta._filters[ 'test_any' ],
            descriptor.Any )

        return inst_filter

    def test_instanciate_filter_model_meta( self ):
        inst_filter = Filter_model_meta()

        self.assertIsInstance( inst_filter._meta._model, Mock )
        self.assertEqual( inst_filter._meta._filters, {} )

        return inst_filter

    def test_instanciate_filter_descriptor_and_meta( self ):
        inst_filter = Filter_descriptor_and_meta()

        self.assertIsInstance( inst_filter._meta._model, Mock )

        self.assertIsInstance(
            inst_filter._meta._filters[ 'test_descriptor' ],
            descriptor.Descriptor )
        self.assertIsInstance(
            inst_filter._meta._filters[ 'test_any' ],
            descriptor.Any )

        return inst_filter

    def test_intenciate_filter_with_inner_filters( self ):
        instance_filter = Filter_with_inner()
        self.assertIn( 'test_filter_inner', instance_filter._meta._filters )
        self.assertIsInstance(
            instance_filter._meta._filters[ 'test_filter_inner' ], dict )

        inner_filters = instance_filter._meta._filters[ 'test_filter_inner' ]
        self.assertIn( 'test_descriptor', inner_filters )
        self.assertIn( 'test_any', inner_filters )

    def test_intenciate_filter_with_nested_filters( self ):
        instance_filter = Filter_with_nested()
        self.assertIn( 'test_filter_nested', instance_filter._meta._filters )
        self.assertIsInstance(
            instance_filter._meta._filters[ 'test_filter_nested' ], dict )

        nested_filters = instance_filter._meta._filters[ 'test_filter_nested' ]
        self.assertIn( 'test_descriptor', nested_filters )
        self.assertIn( 'test_any', nested_filters )

    def test_intenciate_filter_with_nested_filters_filters_are_nested( self ):
        instance_filter = Filter_with_nested()
        nested_filters = instance_filter._meta._filters[ 'test_filter_nested' ]
        self.assertTrue( nested_filters['test_descriptor'].is_in_nested )
        self.assertTrue( nested_filters['test_any'].is_in_nested )
