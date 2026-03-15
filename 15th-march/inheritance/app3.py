# functions -> directly -> file
# class -> holder of a functional aspect (variables)

# making this multi - level

class Animal:
    def eat(self):
        print("eating")

class Dog(Animal):
    def bark(self):
        print("Barking")

class puppy(Dog):
    def sound(self):
        print("weep weep")


puppy_obj = puppy()
puppy_obj.bark()
puppy_obj.eat()
puppy_obj.sound()
