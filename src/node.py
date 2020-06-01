''''

조건문
true
    - child node
    - assign list
false
    - child node
    - assign list


'''
from ast import dump, parse

import astunparse
import astor


class Node:
    index = 1

    def __Init__(self):
        self.parent
        self.before
        self.type
        self.test
        self.true_child
        self.false_child

    def add_to_end(self, new_node):
        new_node = new_node.copy()
        if not hasattr(self, "type"):
            if hasattr(new_node, "before"):
                self.before.extend(new_node.before)
            if hasattr(new_node, "type"):
                self.type = new_node.type
            if hasattr(new_node, "test"):
                self.test = new_node.test
            if hasattr(new_node, "true_child"):
                self.true_child = new_node.true_child
                self.true_child.parent = self
            if hasattr(new_node, "false_child"):
                self.false_child = new_node.false_child
                self.false_child.parent = self
        else:
            if hasattr(self, "true_child"):
                self.true_child.add_to_end(new_node)
            else:
                self.true_child = new_node.copy()
                self.true_child.parent = self
            if hasattr(self, "false_child"):
                self.false_child.add_to_end(new_node)
            else:
                self.false_child = new_node.copy()
                self.false_child.parent = self
        
    def add_loop(self, new_node):
        new_node = new_node.copy()
        flag = False
        if hasattr(self, "before"):
            for x in self.before:
                if dump(x) == "Break()":
                    # TODO return 같은걸로 loop나가는거도 추가
                    print("Break~~~~")
                    flag = True
                if flag:
                    self.before.remove(x)
        if flag:
            return
        
        if not hasattr(self, "type"):
            print("added to existing")
            if hasattr(new_node, "before"):
                self.before.extend(new_node.before)
            if hasattr(new_node, "type"):
                self.type = new_node.type
            if hasattr(new_node, "test"):
                self.test = new_node.test
            if hasattr(new_node, "true_child"):
                self.true_child = new_node.true_child
                self.true_child.parent = self
            if hasattr(new_node, "false_child"):
                self.false_child = new_node.false_child
                self.false_child.parent = self
        else:
            print("add new")
            if hasattr(self, "true_child"):
                self.true_child.add_loop(new_node)
            else:
                self.true_child = new_node.copy()
                self.true_child.parent = self
            if hasattr(self, "false_child"):
                self.false_child.add_loop(new_node)
            else:
                self.false_child = new_node.copy()
                self.false_child.parent = self
        
    def copy(self):
        new_node = Node()
        if hasattr(self, 'before'):
            new_node.before = self.before
        if hasattr(self, 'type'):
            new_node.type = self.type
        if hasattr(self, 'test'):
            new_node.test = self.test
        if hasattr(self, 'true_child'):
            new_node.true_child = self.true_child.copy()
        if hasattr(self, 'false_child'):
            new_node.false_child = self.false_child.copy()
        
        return new_node
    
    def getReverseTest(self):
        return parse("not (" + astunparse.unparse(self.test) + ")").body[0]
    
    def print_test_case(self, prefix, before_list):
        self.index = Node.index
        Node.index += 1
        
        tmp1 = []
        tmp2 = []
        tmp1.extend(before_list)
        tmp2.extend(before_list)
        if hasattr(self, 'before'):
            tmp1.extend(self.before)
            tmp2.extend(self.before)
            
        if hasattr(self, 'type'):
            if hasattr(self, 'true_child'):
                if hasattr(self, 'test'):
                    tmp1.append(self.test)
                self.true_child.print_test_case(str(self.index) + "T", tmp1)
            if hasattr(self, "false_child"):
                if hasattr(self, 'test'):
                    tmp2.append(self.getReverseTest())
                self.false_child.print_test_case(str(self.index) + "F", tmp2)
        else:
            answer = []
            
            # in this case, tmp1=tmp2
            predicates = []
            assigns = []
            for x in tmp1:
                predicate = astunparse.unparse(x).strip()
                if predicate != '':
                    if 'Compare' in dump(x):
                        for y in assigns:
                            if y.targets[0].id in predicates:
                                predicate.replace(y.targets[0].id, dump(y.value))
                        predicates.append(predicate)
                        
                    elif type(x) == 'Assign':
                        assigns.append(x)
            
            for x in predicates:
                print(predicates)
            
            answer = [[1], [100001, 100003, 10005], [1]]
            print(prefix + ": ")
            
            flag = True
            for x in answer[0]:
                for y in answer[1]:
                    for z in answer[2]:
                        flag = True
                        for predicate in predicates:
                            if not eval(predicate):
                                flag = False
                                break;
                        if flag:
                            # success
                            print(prefix, " : ", x, " ", y, " " , z)
                            return
            if not flag:
                print(prefix , " : -")
            # TODO
    
    def to_string(self):
        ret = "{"
        if hasattr(self, 'type'):
            ret += "\"type\":\"" + self.type + "\","
        if hasattr(self, 'test'):
            ret += "\"test\":\"" + dump(self.test) + "\","
        if hasattr(self, 'before'):
            ret += "\"before\":[";
            for x in self.before:
                ret += "\"" + dump(x) + "\","
            ret += "],"
        if hasattr(self, 'true_child'):
            ret += "\"true\":" + self.true_child.to_string() + ","
        if hasattr(self, 'false_child'):
            ret += "\"false\":" + self.false_child.to_string() + ","
        
        return ret + "}"
