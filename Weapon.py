up = "e"
down = "q"
class Weapon:
    def __init__(self):
        self.weapon = 1
    def switch_weapon(self, key):
        if key == up:
            self.weapon += 1
            if self.weapon > 5:
                self.weapon = 1
        elif key == down:
            self.weapon -= 1
            if self.weapon < 1:
                self.weapon = 5
        elif 1 <= key <= 5:
            self.weapon = key

class Revolver(Weapon):
    def __init__(self):
        self.model = model
        self.texture = texture
    def  shooting(self):
        #shootingfunction
        print("shot")