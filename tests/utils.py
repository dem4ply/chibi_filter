from unittest import TestCase
from chibi_filter.utils import Node


class Test_Node( TestCase ):
    def test_init( self ):
        node = Node()
        self.assertFalse( node.negate )
        self.assertFalse( node.children )
        self.assertEqual( node.op, 'AND' )
        return node

    def test_not( self ):
        node = self.test_init()
        not_node = ~node

        self.assertIsNot( not_node, node )
        self.assertTrue( not_node.negate )
        self.assertListEqual( not_node.children, node.children )
        self.assertEqual( node.op, not_node.op )

        return not_node

    def test_and( self ):
        node_1 = Node()
        node_2 = Node()

        node_and = node_1 & node_2

        self.assertIsNot( node_and, node_1 )
        self.assertIsNot( node_and, node_2 )

        self.assertEqual( node_and.op, Node.AND )

        self.assertIs( node_and.children[0], node_1 )
        self.assertIs( node_and.children[1], node_2 )

        return node_and

    def test_or( self ):
        node_1 = Node()
        node_2 = Node()

        node_or = node_1 | node_2

        self.assertIsNot( node_or, node_1 )
        self.assertIsNot( node_or, node_2 )

        self.assertEqual( node_or.op, Node.OR )

        self.assertIs( node_or.children[0], node_1 )
        self.assertIs( node_or.children[1], node_2 )

        return node_or

    def test_join_2_nodes( self ):
        node_1 = self.test_and()
        node_2 = self.test_or()

        node_3 = node_1 & node_2

        self.assertIsNot( node_3, node_1 )
        self.assertIsNot( node_3, node_2 )

        self.assertEqual( node_3.op, Node.AND )

        self.assertIs( node_3.children[0], node_1 )
        self.assertIs( node_3.children[1], node_2 )

    def test_to_dict( self ):
        node = Node()
        result = node.to_dict()
        expected = {
            'op': 'AND',
            'negate': False,
            'childrens': []
        }
        self.assertDictEqual( result, expected )

    def test_to_dict_and( self ):
        node = self.test_and()
        result = node.to_dict()
        expected = {
            'op': 'AND',
            'negate': False,
            'childrens': [
                { 'op': 'AND', 'negate': False, 'childrens': [] },
                { 'op': 'AND', 'negate': False, 'childrens': [] },
            ]
        }
        self.assertDictEqual( result, expected )

    def test_to_dict_or( self ):
        node = self.test_or()
        result = node.to_dict()
        expected = {
            'op': 'OR',
            'negate': False,
            'childrens': [
                { 'op': 'AND', 'negate': False, 'childrens': [] },
                { 'op': 'AND', 'negate': False, 'childrens': [] },
            ]
        }
        self.assertDictEqual( result, expected )
