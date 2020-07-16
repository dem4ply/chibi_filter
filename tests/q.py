from unittest import TestCase
from chibi_filter import Q
from chibi_filter.q import Q_node


class Test_q_tree( TestCase ):
    def test_simple_q( self ):
        q = Q( stuff='somthing' )
        self.assertEqual( q.lookup, { 'stuff': 'somthing' } )
        self.assertFalse( q.children )

    def test_join_to_q( self ):
        q_1 = Q( stuff='somthing' )
        q_2 = Q( nothing='' )

        q_3 = q_1 & q_2
        self.assertIsInstance( q_3, Q_node )
        self.assertIs( q_3.children[0], q_1 )
        self.assertIs( q_3.children[1], q_2 )

        return q_3

    def test_negate_q( self ):
        q = Q( stuff='somthing' )
        q_not = ~q
        self.assertIsInstance( q_not, Q )
        self.assertIsNot( q_not, q )
        self.assertTrue( q_not.negate )
        q_not_not = ~q_not
        self.assertFalse( q_not_not.negate )

    def test_to_dict( self ):
        q = Q( stuff='somthing' )
        result = q.to_dict()
        expected = {
            'op': 'AND',
            'negate': False,
            'lookup': { 'stuff': 'somthing' }
        }
        self.assertDictEqual( result, expected )

    def test_to_dict_and( self ):
        q = self.test_join_to_q()
        result = q.to_dict()
        expected = {
            'op': 'AND',
            'negate': False,
            'childrens': [
                { 'op': 'AND', 'negate': False,
                  'lookup': { 'stuff': 'somthing' } },
                { 'op': 'AND', 'negate': False, 'lookup': { 'nothing': '' } },
            ]
        }
        self.assertDictEqual( result, expected )
