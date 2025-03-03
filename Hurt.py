class Hurt:
    def __init__(self, pos, v):
        self.pos = pos
        self.v = v
    def movement(self):
        self.pos += self.v
class Projectile(Hurt):
    def __init__(self, pos):
        super().__init__(pos)

class RevolverBullet(Projectile):
    def _init_(self, hostility, pos):
        self.hostility = hostility
        self.texture = texture
        self.model = model
        super().__init__(pos)
    def hitevent(self):
        print("hiteventrevolverbullet")


class AreaEffect(Hurt):
    def __init__(self, pos):
        super().__init__(pos)

class PoisonOrb(AreaEffect):
    def _init_(self, hostility, pos):
        self.hostility = hostility
        self.texture = texture
        self.model = model
        super().__init__(pos)
    def hitevent(self):
        print("hiteventpoisonorb")