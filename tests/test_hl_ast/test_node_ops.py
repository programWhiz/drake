from src.hl_ast import Node, VarScope


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


def test_node_insert_before():
    n0, n1, n2, n3, n4, n5 = [ Node() for _ in range(6) ]
    s = VarScope('test', children=[ n1, n2, n5 ])

    s.insert_instrs_before(n5, n4)
    assert s.children == [ n1, n2, n4, n5 ]

    s.insert_instrs_before(n4, n3)
    assert s.children == [ n1, n2, n3, n4, n5 ]

    s.insert_instrs_before(n1, n0)
    assert s.children == [ n0, n1, n2, n3, n4, n5 ]


def test_node_insert_after():
    n0, n1, n2, n3, n4, n5 = [ Node() for _ in range(6) ]
    s = VarScope('test', children=[ n0, n2, n4 ])

    s.insert_instrs_after(n4, n5)
    assert s.children == [ n0, n2, n4, n5 ]

    s.insert_instrs_after(n2, n3)
    assert s.children == [ n0, n2, n3, n4, n5 ]

    s.insert_instrs_after(n0, n1)
    assert s.children == [ n0, n1, n2, n3, n4, n5 ]


def test_node_insert_before_nested():
    n0, n1, n2, n3, n4, n5 = [ Node() for _ in range(6) ]

    n0.children = [ n5 ]
    n5.parent = n0

    n5.children = [ n2, n3 ]
    n2.parent, n3.parent = n5, n5

    s = VarScope('test', children=[ n0, n4 ])

    n3.insert_instrs_before(n3, n1)
    assert s.children == [ n1, n0, n4 ]


def test_node_insert_after_nested():
    n0, n1, n2, n3, n4, n5 = [ Node() for _ in range(6) ]

    n0.children = [ n5 ]
    n5.parent = n0

    n5.children = [ n2, n3 ]
    n2.parent, n3.parent = n5, n5

    s = VarScope('test', children=[ n0, n4 ])

    n3.insert_instrs_after(n3, n1)
    assert s.children == [ n0, n1, n4 ]

