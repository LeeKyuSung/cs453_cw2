''''

조건문
true
    - child node
    - assign list
false
    - child node
    - assign list


'''
from ast import dump


class Node:

    def __Init__(self):
        self.before
        self.type
        self.test
        self.true_child
        self.false_child

    def add_to_end(self, new_node):
        if not hasattr(self, "type"):
            if hasattr(new_node, "before"):
                self.before.extend(new_node.before)
            if hasattr(new_node, "type"):
                self.type = new_node.type
            if hasattr(new_node, "test"):
                self.test = new_node.test
            if hasattr(new_node, "true_child"):
                self.true_child = new_node.true_child
            if hasattr(new_node, "false_child"):
                self.false_child = new_node.false_child
        else:
            if hasattr(self, "true_child"):
                self.true_child.add_to_end(new_node)
            else:
                self.true_child = new_node.copy()
            if hasattr(self, "false_child"):
                self.false_child.add_to_end(new_node)
            else:
                self.false_child = new_node.copy()
        
    def copy(self):
        new_node = Node()
        if hasattr(self, 'before'):
            new_node.before = self.before
        if hasattr(self, 'type'):
            new_node.type = self.type
        if hasattr(self, 'test'):
            new_node.test = self.test
        if hasattr(self, 'true_child'):
            new_node.true_child = self.true_child
        if hasattr(self, 'false_child'):
            new_node.false_child = self.false_child
        
        return new_node
    
    def to_string(self):
        ret = "{"
        if hasattr(self, 'type'):
            ret += "\"type\":\"" + self.type + "\","
        if hasattr(self, 'test'):
            ret += "\"test\":\"" + dump(self.test) + "\","
        if hasattr(self, 'before'):
            ret += "\"before\":[";
            for x in self.before:
                ret += "\""+dump(x)+"\","
            ret += "],"
        if hasattr(self, 'true_child'):
            ret += "\"true\":" + self.true_child.to_string() + ","
        if hasattr(self, 'false_child'):
            ret += "\"false\":" + self.false_child.to_string() + ","
        
        return ret + "}"
