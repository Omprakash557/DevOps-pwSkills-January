# functions -> directly -> file
# class -> holder of a functional aspect (variables)

class Animal:
    def eat(self):
        print("eating")

class Dog(Animal):
    def bark(self):
        print("Barking")

'''  we didnt called the function
bark() -> this way is of calling function outside of any class (classless function)
eat()
'''

# for calling a function within a class we need objects (self ref)
# d -> name of object (self -> point to functions)
# Dog() -> class Name
d = Dog()
d.eat()
