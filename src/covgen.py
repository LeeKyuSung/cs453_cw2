'''
Created on 2020. 5. 27.

@author: LeeKyuSung
'''

from _ast import FunctionDef, Assign, If, AnnAssign, AugAssign, For, While, \
    Return
from ast import dump
from unittest import case

from astor import parse_file
from astor.code_gen import to_source
from astor.node_util import dump_tree, iter_node

from node import Node

# 1. 파일 읽기
targetFile = "../inputs/sample6.py"
ast = parse_file(targetFile)
# print(dump(ast))

# 2. 파일 내용 조건 확인
# test_me function 탐색
# arguments integer만 받는지
body = ast.body
is_test_able = False
function_def = None
for x in body:
    if type(x) == FunctionDef:
        if x.name == "test_me":
            is_test_able = True
            function_def = x
            break
        
# TODO argument 체크

if is_test_able:
    print("is_test_able : True")
else:
    print("is_test_able : False")
    exit()


# 3. 테스트 할 function 분석해서 tree로 바꾸고, root 저장
def make_node(list):
    node = Node()
    
    before = []
    
    index = -1
    for x in list:
        index += 1
        t = type(x)
        if t == If:
            node.type = "If"
            node.test = x.test
            node.true_child = make_node(x.body)
            node.false_child = make_node(x.orelse)
            break;
        else:
            before.append(x)
    
    new_list = []
    if len(list)!=0 and index+1!=len(list):
        for i in range(index+1, len(list)):
            new_list.append(list[i])
        node.add_to_end(make_node(new_list))
    
    node.before = before
    
    return node
    

root = make_node(function_def.body)

# 4. 각 노드별로 테스트 케이스 생성
# 사용 안하는 값은 뭘로 넣지? 일단 랜덤으로 시도해보자

print(root.to_string())
