#!/usr/bin/env python3

import sys

class Calculator:
    def add(self, x, y):
        return x + y

    def increment(self, x):
        x += 1
        return x
 
if __name__=='__main__':
    #creating object of class
    calculator = Calculator()
    #capturing input from command line and casting to integer
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    z = calculator.add(x, y)
    #printing result on console
    print(z)