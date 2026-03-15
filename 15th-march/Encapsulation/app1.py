# encap sulation
# with in one class - full control
# functions + variables ( controls)

class Student:
    # constructor -> is called when the object is created
    # obj_student -> Default ( name, marks)

    def __init__(self,name,marks):
        self.name = name # public varaible (anywhere can access)
        self.__marks = marks # private variable ( __)

        # keep the name public and hide the marks
    def get_marks(self):
        return self.__marks
    
    def set_marks(self,marks):
        if marks >= 0 and marks <=100:
            self.__marks = marks
        else:
            print("Invalid marks")

s1 = Student("Rahul",85)

# access using getter
print("Marks:", s1.get_marks)
# setter -> setting the value
s1.set_marks(90)
print("Updated Marks:",s1.get_marks())