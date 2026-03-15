class Animal():
    def sound(self):
        print("Animal makes sound")

class Dog(Animal):
    def sound(self):
        print("Dog makes sound")


class Cat(Animal):
    def sound(self):
        print("Cat makes sound")

Animal_object = Animal()
Animal_object.sound()

Dog_Object = Dog()
Dog_Object.sound()

Cat_Object = Cat()
Cat_Object.sound()