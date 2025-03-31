import random
import glm

# Gegner Definitionen. Plop wird im Spiel genutzt.

class Enemy:
    def __init__(self, pos, hp, speed):
        self.pos = pos
        self.hp = hp
        self.idlew = 0
        self.idlea = 0
        self.walkingt = 0
        self.v = glm.vec3(0.0, 0.0, 0.0)
        self.projectiles = []
        self.speed = speed

class Plop(Enemy):
    def __init__(self, model_id, pos: glm.vec3):
        super().__init__(pos, 3, 0.1)
        self.model_id = model_id
    def action(self, frametime, targetpos):
        if self.idlew <= 0:
            self.vv = glm.vec3(random.randint(-1, 1), 0, random.randint(-1, 1)) * 2
            self.walkingt = random.randint(1, 2)
            self.idlew = random.randint(0, 3)
        if self.walkingt > 0:
            self.v = glm.normalize(self.vv + glm.normalize(targetpos - self.pos) * 3) * 3
            self.v[1] = 0
            if glm.distance(self.pos, targetpos) > 10:
                self.pos += self.v * frametime
            self.walkingt -= 1 * frametime
        elif self.idlew > 0:
            self.idlew -= 1  * frametime

    
        
