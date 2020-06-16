from sympy.solvers import solve
from sympy import Symbol

from ast import dump
from builtins import staticmethod

class SymGen:
    @staticmethod
    def convert_to_equation(str):
        if str.contains("=="):
            str.replace("==", "=")
        if str.contains("and"):
            str.replace("and", "&")
        if str.contains("or"):
            str.replace("or", "|")
        
    @staticmethod
    def generate_answer(predicates, args):
        print("LOG : predicates")
        index = 0
        for x in predicates:
            index = index + 1
            print(index, " : " , x)
        
        print("LOG : args")
        index = 0
        for x in args:
            index = index + 1
            print(index, " : ", dump(x))
    
        # add symbol
        for x in args:
            Symbol(x.arg)
        # predicates solve
        #predicate = ''
        #for x in predicates:
            #predicate = predicate +  
         