'''
loops example:
for loop -> run when we know the number of iterations

while loop -> run when we know the condition
'''

# for loop uses a function called as range()
# range(start, stop, step)
# start -> starting point of the loop (default is 0)
# stop -> ending point of the loop (not included in the loop)
# step -> increment or decrement value (default is 1)

# range(0,5) -> 0,1,2,3,4
# range(0,5,1) -> 0,1,2,3,4
# range(5,0,-1) -> 5,4,3,2,1
# range(0,10,2) -> 0,2,4,6,8

'''
for i in range(0,5):
    print(i)
'''
print("======")

'''
for i in range(5,0,-1):
    print(i)

    5 -> starting (inclusive)
    0 -> ending 

'''

for i in range(0,5,1):
    print(i)


# range (python) -> 0 - 5 (0,... 4)