from src.visitor import Visitor
import re
import os


class Generator(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.py = ""
        self.level = 0

    def append(self, text):
        self.py += str(text)

    def newline(self):
        self.append('\n\r')

    def indent(self):
        for i in range(self.level):
            self.append('\t')

    def visit_Program(self, parent, node):
        for n in node.nodes:
            self.visit(node, n)
        self.append('if __name__ == "__main__":')
        self.newline()
        self.level += 1
        self.indent()
        self.append('main()')
        self.newline()
        self.level -= 1

    def visit_Decl(self, parent, node):
        pass

    def visit_Assign(self, parent, node):
        self.visit(node, node.id_)
        self.append(' = ')
        self.visit(node, node.expr)

    def visit_If(self, parent, node):
        self.append('if ')
        self.visit(node, node.cond)
        self.append(':')
        self.newline()
        self.visit(node, node.true)
        if node.false is not None:
            self.indent()
            self.append('else:')
            self.newline()
            self.visit(node, node.false)

    def visit_While(self, parent, node):
        self.append('while ')
        self.visit(node, node.cond)
        self.append(':')
        self.newline()
        self.visit(node, node.block)

    def visit_FuncImpl(self, parent, node):
        self.append('def ')
        self.append(node.id_.value)
        self.append('(')
        self.visit(node, node.params)
        self.append('):')
        self.newline()
        self.visit(node, node.block)

    def visit_FuncCall(self, parent, node):
        func = node.id_.value
        args = node.args.args
        if func == 'print':
            format_ = args[0].value
            matches = re.findall('%[dcs]', format_)
            format_ = re.sub('%[dcs]', '{}', format_)
            self.append('print("')
            self.append(format_)
            self.append('"')
            if len(args) > 1:
                self.append('.format(')
                for i, a in enumerate(args[1:]):
                    if i > 0:
                        self.append(', ')
                    if matches[i] == '%c':
                        self.append('chr(')
                        self.visit(node.args, a)
                        self.append(')')
                    elif matches[i] == '%s':
                        self.append('"".join([chr(x) for x in ')
                        self.visit(node.args, a)
                        self.append('])')
                    else:
                        self.visit(node.args, a)
                self.append(')')
            self.append(', end="")')
        
        
       
        else:
            self.append(func)
            self.append('(')
            self.visit(node, node.args)
            self.append(')')

    def visit_Block(self, parent, node):
        self.level += 1
        for n in node.nodes:
            self.indent()
            self.visit(node, n)
            self.newline()
        self.level -= 1

    def visit_Params(self, parent, node):
        for i, p in enumerate(node.params):
            if i > 0:
                self.append(', ')
            self.visit(p, p.id_)


    def visit_Elems(self, parent, node):
        for i, e in enumerate(node.elems):
            if i > 0:
                self.append(', ')
            self.visit(node, e)

    def visit_Type(self, parent, node):
        pass

    def visit_Int(self, parent, node):
        self.append(node.value)

    def visit_Char(self, parent, node):
        self.append(ord(node.value))

    def visit_String(self, parent, node):
        self.append(node.value)

    def visit_Id(self, parent, node):
        self.append(node.value)

    def visit_BinOp(self, parent, node):
        self.visit(node, node.first)
        if node.symbol == '&&':
            self.append(' and ')
        elif node.symbol == '||':
            self.append(' or ')
        elif node.symbol == '/':
            self.append('//')
        else:
            self.append(node.symbol)
        self.visit(node, node.second)

    def visit_UnOp(self, parent, node):
        if node.symbol == '!':
            self.append('not ')
        elif node.symbol != '&':
            self.append(node.symbol)
        self.visit(node, node.first)

    def generate(self, path):
        self.visit(None, self.ast)
        self.py = re.sub('\n\s*\n', '\n', self.py)
        with open(path, 'w') as source:
            source.write(self.py)
        return path
