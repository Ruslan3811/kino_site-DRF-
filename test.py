class Pizza:
    def __init__(self, name):
        self.name = name
        self.radius = radius

    def make_pizza(self):
        print("Maing pizza")

    make_pizza.add_more_cheese = 300
    # def adding_more_cheese(cls):
    #     return cls

class Mozzarella(Pizza):

    def __init__(self, name):
        self.name = name



mozzarella = Mozzarella("Mozzarella")
# print(Mozzarella.add_more_cheese)
print(mozzarella.make_pizza.add_more_cheese)