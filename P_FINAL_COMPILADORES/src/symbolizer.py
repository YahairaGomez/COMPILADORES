from src.visitor import Visitor
from src.symbols import Symbols
from src.NodosVariab import *


class Symbolizer(Visitor):
    def __init__(self, ast):
        self.ast = ast

    def visit_Program(self, parent, node):
        node.symbols = Symbols()
        for n in node.nodes:
            self.visit(node, n)

    def visit_Decl(self, parent, node):
        parent.symbols.put(node.id_.value, node.type_.value, id(parent))
   
    def visit_Assign(self, parent, node):
        pass

    def visit_If(self, parent, node):
        self.visit(node, node.true)
        if node.false is not None:
            self.visit(node, node.false)

    def visit_While(self, parent, node):
        self.visit(node, node.block)

    def visit_FuncImpl(self, parent, node):
        parent.symbols.put(node.id_.value, node.type_.value, id(parent))
        self.visit(node, node.block)
        self.visit(node, node.params)

    def visit_FuncCall(self, parent, node):
        pass

    def visit_Block(self, parent, node):
        node.symbols = Symbols()
        for n in node.nodes:
            self.visit(node, n)

    def visit_Params(self, parent, node):
        node.symbols = Symbols()
        for p in node.params:
            self.visit(node, p)
            self.visit(parent.block, p)


    def visit_Elems(self, parent, node):
        pass

    def visit_Type(self, parent, node):
        pass

    def visit_Int(self, parent, node):
        pass

    def visit_Char(self, parent, node):
        pass

    def visit_String(self, parent, node):
        pass

    def visit_Id(self, parent, node):
        pass

    def visit_BinOp(self, parent, node):
        pass

    def visit_UnOp(self, parent, node):
        pass

    def symbolize(self):
        self.visit(None, self.ast)
