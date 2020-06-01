'''
Created on 2020. 5. 27.

@author: LeeKyuSung
'''

from _ast import FunctionDef, Assign, If
from ast import dump

from astor import parse_file
from astor.code_gen import to_source
from astor.node_util import dump_tree, iter_node
import astunparse


targetFile = "../inputs/sample1.py"

ast = parse_file(targetFile)

print(dump(ast))

a = []

body1 = ast.body;
for x in body1:
    if type(x) == FunctionDef:
        name = x.name
        print("NAME : " + name)
        
        args = x.args.args
        print("arg length : " + str(len(args)))
        for y in args:
            print(y.arg)
        
        body = x.body
        for y in body:
            if isinstance(y, If):
                print("[IF]")
                print(y.test.comparators[0].value)
            elif isinstance(y, Assign):
                print("[Assign]")
                a.append(y)
        
        decorator_list = x.decorator_list
        returns = x.returns
        type_comment = x.type_comment


print(a)
for x in a:
    print(dump(x))
    print(astunparse.unparse(x))