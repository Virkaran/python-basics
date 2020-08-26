class Person:
    def __init__(self , name , year ):
        self.name = name
        self.year = year
        self.friends = set()
    
    def add_friends(self ,other_person):
        if not isinstance(other_person ,Person):
            raise TypeError(other_person, 'is not a ',Person)
        self.friends.add(other_person)
        other_person.friends.add(self)

    def __repr__(self):
        return f'Person(name={self.name!r}, '   \
               f'year={self.year!r},'   \
               f'friends = {[f.name for f in self.friends]})'
