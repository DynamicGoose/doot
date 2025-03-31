import glm
import copy

# Projektil-Definitionen, selbsterklärend

class RevolverBullet:
    def __init__(self, model_id, pos: glm.vec3, dir: glm.vec3, speed):
        self.speed = speed
        self.pos = 0
        self.pos += pos
        self.model_id = model_id
        self.v = copy.copy(dir) * self.speed
        self.pos += copy.copy(dir)
    def hitevent(self, target):
        target.hp -= 1


    def rb_movement(self):
        self.pos += self.v


class PoisonOrb:
    def __init__(self, pos, hostility):
        self.hostility = hostility
        self.pos = pos
    def hitevent(self):
        print("hiteventpoisonorb")
    def movement(self):
        self.pos += self.v
