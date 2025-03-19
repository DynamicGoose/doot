import glm
class RevolverBullet:
    def __init__(self, model_id, pos: glm.vec3, targetpos: glm.vec3, hostility):
        self.speed = 10
        self.pos = 0
        self.pos += pos
        self.hostility = hostility
        self.model_id = model_id
        self.targetpos = targetpos
        self.v = glm.normalize(self.targetpos - self.pos) * self.speed
    def hitevent(self):
        print("hiteventrevolverbullet")

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