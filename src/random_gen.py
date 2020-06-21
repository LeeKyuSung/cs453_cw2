from ast import dump
from builtins import staticmethod
from random import randrange
import sys, time

class RandomGen:
    @staticmethod
    def generate_answer(predicates, args):
        start_time = time.time()
        
        while True:
            # if it tooks so long, stop
            if time.time()-start_time > 5 :
                return []
            
            # generate random answer & assign to each value
            trying = []
            for arg in args:
                random = randrange(-sys.maxsize-1, sys.maxsize)
                trying.append(random)
                exec(arg.arg + " = " + str(random))
            # TODO make not to use as arg which used here
            
            # check if it is right answer
            success = True
            for predicate in predicates:
                if not eval(predicate):
                    success = False
                    break
            if success:
                return trying