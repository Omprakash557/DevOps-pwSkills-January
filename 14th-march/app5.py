# function

'''
functions are the way of doing / writing modularize / reusable
code in python

def function_name(parameters):
    # function body
    return value



def print_eligible():
    print("You are eligible to vote")

def not_print_eligible():
    print("You are not eligible to vote")

age = int(input("enter your age: "))

if age >= 18:
    print_eligible()
else:
    not_print_eligible()


    '''
# function with parameters


def sum_marks(marks1,marks2):
    total = marks1 + marks2
    return total    

# function name =   sum_marks  
# parameters = marks1, marks2
# function body = total = marks1 + marks2
# return value = total
print(sum_marks(100,200))