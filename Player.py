import glm

class Player:
    def __init__(self, pos, hp):
        self.pos = pos
        self.hp = hp
        self.v = [0.0, 0.0, 0.0]
        self.a = 1
        self.maxv = 10
        self.d = [0.0, 0.0, 0.0]
    def horizontal_movement(self):
        if (self.v[0] ** 2  + self.v[1] ** 2) // 2  < self.maxv:
            self.v[0, 1] += self.d[0, 1] * self.a
    def vertical_movement(self):
        self.v[2] += g
        #if spacebar pressed and on the floor:
        #   self.v[2] = jumping_strength
        #if self.pos + self.v[2] through floor:
        #   self.pos[2] on floor
        #   self.v[2] = 0.0