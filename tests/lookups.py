from unittest import TestCase
from chibi_filter.lookup import Lookup


class Test_lookup( TestCase ):

    def test_init( self ):
        lookup = Lookup( 'some_field', 'eq', 'nothign' )
        return lookup

    def test_build( self ):
        lookup = self.test_init()
        with self.assertRaises( NotImplementedError ):
            lookup.build()

