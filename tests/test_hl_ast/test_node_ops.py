from src.hl_ast import Node


def test_node_replace_empty():
    n1, n2 = Node(), Node()
    n3 = Node(children=[ n1, n2 ])
    n3.replace_child(n2, [])
    assert n3.children == [ n1 ]


def test_node_replace_single():
    n1, n2 = Node(), Node()
    n3 = Node(children=[ n1, n2 ])
    n4 = Node()
    n3.replace_child(n2, [ n4 ])
    assert n3.children == [ n1, n4 ]


def test_node_replace_multi():
    n1, n2, n3, n4 = Node(), Node(), Node(), Node()
    n5 = Node(children=[ n1, n2 ])
    n5.replace_child(n2, [ n3, n4 ])
    assert n5.children == [ n1, n3, n4 ]
    n5.replace_child(n1, [ n3, n2 ])
    assert n5.children == [ n3, n2, n3, n4 ]