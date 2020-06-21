from _ast import If, While, For
from ast import dump, parse

import astunparse

from improved_gen import ImprovedGen
from random_gen import RandomGen


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
        
    def add_loop(self, num, new_node):
        # break 있는지 체크
        flag = False
        if hasattr(self, "before"):
            for x in self.before:
                if flag:
                    self.before.remove(x)
                if dump(x) == "Break()":
                    flag = True
        if flag:
            return
        
        if not hasattr(self, "type"):
            new_node = new_node.copy()
            if hasattr(new_node, "type"):
                self.type = new_node.type
            if hasattr(new_node, "test"):
                self.test = new_node.test
            if hasattr(new_node, "true_child"):
                self.true_child = new_node.true_child
                self.true_child.parent = self
                if num>1:
                    self.true_child.add_loop(num-1, new_node)
            if hasattr(new_node, "false_child"):
                self.false_child = new_node.false_child
                self.false_child.parent = self
        else:
            if hasattr(self, "true_child"):
                if num>1:
                    self.true_child.add_loop(num-1, new_node)
            else:
                self.true_child = new_node.copy()
                self.true_child.parent = self
                if num>1:
                    self.true_child.add_loop(num-1, new_node)
            if hasattr(self, "false_child"):
                if num>1:
                    self.false_child.add_loop(num-1, new_node)
            else:
                self.true_child = new_node.copy()
                self.true_child.parent = self
                if num>1:
                    self.false_child.add_loop(num-1, new_node)
        
    def copy(self):
        new_node = Node()
        if hasattr(self, 'before'):
            new_node.before = self.before[:]
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
    
    def print_test_case(self, prefix, before_list, args):
        self.index = Node.index
        Node.index += 1
        
        before_list_true = []
        before_list_false = []
        before_list_true.extend(before_list)
        before_list_false.extend(before_list)
        if hasattr(self, 'before'):
            before_list_true.extend(self.before)
            before_list_false.extend(self.before)
            
        if hasattr(self, 'type'):
            if hasattr(self, 'true_child'):
                if hasattr(self, 'test'):
                    before_list_true.append(self.test)
                self.true_child.print_test_case(str(self.index) + "T", before_list_true, args)
            if hasattr(self, "false_child"):
                if hasattr(self, 'test'):
                    before_list_false.append(self.getReverseTest())
                self.false_child.print_test_case(str(self.index) + "F", before_list_false, args)
        else:
            # in this case, before_list_true=before_list_false            
            predicates = []
            for x in before_list_true:
                if 'Compare' in dump(x):
                    predicate = astunparse.unparse(x).strip()
                    if predicate != '':
                        predicates.append(predicate)
            
            answer = ImprovedGen.generate_answer(predicates, args)
            
            print(predicates)
            if len(answer) == 0:
                print(prefix, " : -")
            else:
                print(prefix, " : ", end='')
                for x in answer:
                    print(x, " ", end=''),
                print()
    
    def to_string(self):
        # for logging
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
    
    @staticmethod
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
                node.true_child = Node.make_node(x.body)
                node.true_child.parent = node
                node.false_child = Node.make_node(x.orelse)
                node.false_child.parent = node
                break
            elif t == While:
                node.type = "While"
                node.test = x.test
                node.true_child = Node.make_node(x.body)
                node.true_child.parent = node
                node.false_child = Node.make_node(x.orelse)
                node.false_child.parent = node
                
                node.true_child.add_loop(5, node)
                break
            elif t == For:
                continue
            else:
                before.append(x)
        
        new_list = []
        if len(list) != 0 and index + 1 != len(list):
            for i in range(index + 1, len(list)):
                new_list.append(list[i])
            node.add_to_end(Node.make_node(new_list))
        node.before = before
        
        return node
