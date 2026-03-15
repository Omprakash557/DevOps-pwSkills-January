# functions -> directly -> file
# class -> holder of a functional aspect (variables)

# making this multi - level

class Animal:
    def eat(self):
        print("eating")

class Dog(Animal):
    def bark(self):
        print("Barking")

class Cat(Animal):
    def sound(self):
        print("meow meow")


Cat_obj = Cat()
Cat_obj.bark()
Cat_obj.eat()
Cat_obj.sound()
