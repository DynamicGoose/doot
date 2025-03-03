import random
class Enemy:
    def __init__(self, pos, hp):
        self.pos = pos
        self.hp = hp
        self.idlew = 0
        self.idlea = 0
        self.walkingt = 0
        self.v = [0.0, 0.0, 0.0]

class plop(Enemy):
    def __init__(self, model, texture):
        self.model = model
        self.texture = texture
    def action(self):
        if self.idlew <= 0:
            self.v = [0.0, 0.0, 0.0]
            self.walkingt = random.randint(0, 0)

        if self.walkingt > 0:
            #movement function
            self.walkingt -= 1
        elif self.idlew > 0:
            self.idlew -= 1

        if idlea <= 0:
            #attack function
            idlea = random.randint(0, 0)
        else:
            idlea -= 1