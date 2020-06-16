from _ast import FunctionDef, If, While
from astor import parse_file
from node import Node

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
            node.true_child.parent = node
            node.false_child = make_node(x.orelse)
            node.false_child.parent = node
            break;
        elif t == While:
            node.type = "While"
            node.test = x.test
            node.true_child = make_node(x.body)
            node.true_child.parent = node
            node.false_child = make_node(x.orelse)
            node.false_child.parent = node
            
            for tmp in range(0, 5):
                node.true_child.add_loop(node)
            
            break
        else:
            before.append(x)
    
    new_list = []
    if len(list) != 0 and index + 1 != len(list):
        for i in range(index + 1, len(list)):
            new_list.append(list[i])
        node.add_to_end(make_node(new_list))
    
    node.before = before
    
    return node

def find_test_case(function_def):
    
    # arguments 저장
    args = function_def.args.args
    
    # 테스트 할 function 분석해서 tree로 바꾸고, root 저장
    root = make_node(function_def.body)
    print(root.to_string())
    
    # 각 노드별로 테스트 케이스 생성
    root.print_test_case("R", [], args)


# 파일 읽기
targetFile = "../inputs/sample2.py"
ast = parse_file(targetFile)

# function마다 테스트케이스 찾기
body = ast.body
function_def = None
for x in body:
    if type(x) == FunctionDef:
        find_test_case(x)
