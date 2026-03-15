class Father:
    def skills(self):
        print("Gardening")
    

class Mother:
    def hobbies(self):
        print("Cycling")

class Child(Father,Mother):
    pass

child_obj = Child()
child_obj.hobbies()
child_obj.skills()