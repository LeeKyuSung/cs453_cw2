from _ast import FunctionDef
from ast import dump
from astor import parse_file
from node import Node

def find_test_case(function_def):
    print(dump(function_def))
    # arguments 저장
    args = function_def.args.args
    
    # 테스트 할 function 분석해서 tree로 바꾸고, root 저장
    root = Node.make_node(function_def.body)
    print(root.to_string())
    
    # 각 노드별로 테스트 케이스 생성
    root.print_test_case("R", [], args)

# 파일 읽기
targetFile = "../inputs/sample7.py"
ast = parse_file(targetFile)

# function마다 테스트케이스 찾기
body = ast.body
function_def = None
for x in body:
    if type(x) == FunctionDef:
        find_test_case(x)
