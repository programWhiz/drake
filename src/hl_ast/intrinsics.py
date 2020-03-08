from .node import Node


class CallIntrinsic(Node):
    def __init__(self, intrinsic:str=None, **kwargs):
        super().__init__(**kwargs)
        self.intrinsic = intrinsic

    def to_ll_ast(self):
        args = [ child.to_ll_ast() for child in self.children ]
        return { "op": "call", "intrinsic": self.intrinsic, "args": args }


class Printf(CallIntrinsic):
    def __init__(self, **kwargs):
        kwargs['intrinsic'] = 'printf'
        super().__init__(**kwargs)
