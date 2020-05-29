'''
Created on 2020. 5. 27.

@author: LeeKyuSung
'''

from _ast import FunctionDef, Assign, If
from ast import dump

from astor import parse_file
from astor.code_gen import to_source
from astor.node_util import dump_tree, iter_node


targetFile = "../inputs/sample1.py"

ast = parse_file(targetFile)

print(dump(ast))

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
        
        decorator_list = x.decorator_list
        returns = x.returns
        type_comment = x.type_comment

'''

1. 파일 읽기
2. 조건 맞는지 확인
3. function def (test_me) 있는지 확인
4. 해당 function 재귀로 tree 생성
5. 각 노드 별로 테스트 케이스 생성
-> 사용안하는 값은 뭘로 넣지? 일단 랜덤으로 하고 생각해보자

'''