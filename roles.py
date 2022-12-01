from typing import Union

class Ingredient():
    def __init__(self, value: str):
        self.value = value
    def new_one(self):
        return Ingredient(self.value)

class Dish:
    def __init__(self):
        self.content: Union[list[Ingredient], None] = None
    def new_one(self):
        return Dish()

class Pot:
    def __init__(self):
        self.need_cooking = 0
        self.soup: list[Ingredient] = []

    def cooking(self):
        self.need_cooking -= 1

    def dump(self):
        if self.need_cooking != 0:
            return None
        if len(self.soup) == 3:
            soup, self.soup = self.soup, []
            return soup

    def add(self, ingred: Ingredient):
        if len(self.soup) >= 3:
            return False
        self.soup.append(ingred)
        # self.need_cooking += 5
        return True

class Server:
    def __init__(self, can_serve_ingredient: bool):
        self.serve_ingredient = can_serve_ingredient
    def serve(self, dish: Union[Dish, Ingredient]):
        success, reward = False, 0
        if type(dish) is Ingredient and self.serve_ingredient:
            success, reward = True, 1
        elif type(dish) is Dish and dish.content != None and len(dish.content) == 3:
            success, reward = True, 1
        return success, reward

class Counter:
    def __init__(self, holding: Union[Pot, Ingredient, Dish, Server, None]):
        self.holding = holding
        self.new_one_to_dispense = False


class Chef:
    def __init__(self):
        self.holding: Union[Ingredient, Dish, None] = None

    def interact(self, counter: Counter):
        reward = 0
        if self.holding == None:
            if type(counter.holding) in [Dish, Ingredient]:
                if counter.new_one_to_dispense:
                    self.holding = counter.holding.new_one()
                else:
                    self.holding, counter.holding = counter.holding, None
        elif type(self.holding) is Dish:
            if counter.holding == None:
                counter.holding, self.holding = self.holding, None
            elif type(counter.holding) is Pot:
                if self.holding.content == None:
                    self.holding.content = counter.holding.dump()
            elif type(counter.holding) is Server:
                success, reward = counter.holding.serve(self.holding)
                if success:
                    self.holding = None
        elif type(self.holding) is Ingredient:
            if counter.holding == None:
                counter.holding, self.holding = self.holding, None
            elif type(counter.holding) is Pot:
                success = counter.holding.add(self.holding)
                if success:
                    self.holding = None
            elif type(counter.holding) is Server:
                success, reward = counter.holding.serve(self.holding)
                if success:
                    self.holding = None
        return reward



