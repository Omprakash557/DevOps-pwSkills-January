# abstraction is hiding implementation(core functionality)

from abc import ABC, abstractmethod

# pass ABC -> create a abstract class
# each abstract class - should have abstract method

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectange(Shape):
    def __init__(self,length,width):
        self.length = length
        self.width = width
    
    def area(self):
        return self.length * self.width

r = Rectange(2,3)
'''

use Case: companies : which works on algorithm (assets)
Uber / Zomato / Swiggy: assets (logical implement / algorithm)
'''