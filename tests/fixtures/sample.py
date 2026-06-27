import os
import json  # unused

def used_function():
    return os.getcwd()

def dead_function():
    return "nobody calls me"

class UsedClass:
    def method(self):
        return used_function()

class DeadClass:
    pass

active_var = UsedClass()
dead_var = "unused"

result = active_var.method()
