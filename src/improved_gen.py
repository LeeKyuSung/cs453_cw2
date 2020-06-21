from ast import dump, parse
from builtins import staticmethod
from random import randrange
import sys, time
import re

from astor import parse_file


class ImprovedGen:
    @staticmethod
    def generate_answer(predicates, argsssss):
        maxxxx = 0
        for predicate in predicates:
            tmp = re.findall('\d', predicate)
            for xxxx in tmp:
                if int(xxxx)*3 > maxxxx:
                    maxxxx = int(xxxx)*3
        trying = []
        
        start_time = time.time()
        while True:
            # if it tooks so long, stop
            if time.time()-start_time > 1 :
                break
            
            # generate random answer & assign to each value
            trying=[]
            for arg in argsssss:
                random = randrange(-maxxxx-1, maxxxx)
                trying.append(random)
                exec(arg.arg + " = " + str(random))
                
            # check if it is right answer
            success = True
            for predicate in predicates:
                if not eval(predicate):
                    success = False
                    break
            if success:
                break
        
        if len(trying)!=0 and success:
            return trying
        
        start_time = time.time()
        while True:
            # if it tooks so long, stop
            if time.time()-start_time > 10 :
                return []
            
            # generate random answer & assign to each value
            trying=[]
            for arg in argsssss:
                random = randrange(-sys.maxsize-1, sys.maxsize)
                trying.append(random)
                exec(arg.arg + " = " + str(random))
            
            # check if it is right answer
            success = True
            for predicate in predicates:
                if not eval(predicate):
                    success = False
                    break
            if success:
                return trying