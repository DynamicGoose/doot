from renderer.window import CollisionWindow
import glm
import moderngl_window as glw
from Projectile import RevolverBullet
from Enemy import Plop
from Weapon import Revolver
from random import randint

# Spiel-Fenster
class DootWindow(CollisionWindow):
    title = "DOOT"
    resource_dir = "assets"
    fullscreen = False
    vsync = False
    
    def __init__(self, **kwargs):        
        super().__init__("arena/arena.gltf", [["Enemy/enemy.gltf"], [], []], **kwargs)
        self.camera.set_position(0.0, 0.0, 5.0)
        self.camera.velocity = 5.0
        self.jump_vel = 0.0
        self.enemies = [Plop(0, glm.vec3(10, 0, 10))]
        self.projectiles_enemy = []
        self.projectiles_player = []
        self.weapon = Revolver()
        self.mouse_pressed = False
        self.spawn_enemy = False
        self.player_hp = 50
        self.enemy_time = 5
        self.enemy_last_time = 0.0

    # wird für jedes Render aufgerufen
    def on_render(self, time, frametime):
        # einen Gegener jede self.enemy_time spawnen
        if time - self.enemy_last_time >= self.enemy_time:
            self.spawn_enemy = True
            self.enemy_last_time = time

        # Spieler-Waffe
        if self.mouse_pressed:
            self.weapon.shooting(self.camera.dir, self.camera.position, self.projectiles_player)
            self.dynamic_bullet_player.append(self.load_scene("bullet_01/bullet_01.gltf"))
            self.mouse_pressed = False


        # Spieler HP abziehen, falls er getroffen wird
        if self.detect_player_hit():
            print("hit")
            self.player_hp -= 10
            for projectile in self.projectiles_enemy:
                if glm.distance(self.camera.position, projectile.pos) < 1:
                    self.id = projectile.model_id
                    for projectile in self.projectiles_enemy:
                        if self.id < projectile.model_id:
                            projectile.model_id -= 1
                    del self.dynamic_bullet_enemy[projectile.model_id]
                    del self.projectiles_enemy[projectile.model_id]
            if self.player_hp < 0: # game over, wenn der Spieler keine HP mehr hat
                print("game over!")
                exit()

        # Gegner spawnen
        if self.spawn_enemy:
            self.enemies.append(Plop(len(self.dynamic_enemy), glm.vec3(randint(-50, 50), randint(0, 3), randint(-50, 50))))
            self.dynamic_enemy.append(self.load_scene("Enemy/enemy.gltf"))
            self.spawn_enemy = False

        # Überprüfen, welche Gegner getroffen wurden, dann das nächste Spieler-Projektiel löschen
        for enemy_id in self.detect_enemy_hits():
            self.enemies[enemy_id].hp -= 1
            for projectile in self.projectiles_player:
                if glm.distance(self.enemies[enemy_id].pos, projectile.pos) < 1:
                    self.id = projectile.model_id
                    for projectile in self.projectiles_player:
                        if self.id < projectile.model_id:
                            projectile.model_id -= 1
                    del self.dynamic_bullet_player[projectile.model_id]
                    del self.projectiles_player[projectile.model_id]
            # Gegner löschen, wenn 0 HP
            if self.enemies[enemy_id].hp < 1:
                for enemy in self.enemies:
                    if enemy_id < enemy.model_id:
                        enemy.model_id -= 1
                del self.dynamic_enemy[enemy_id]
                del self.enemies[enemy_id]

        # Gegner Movement und Angriff
        for enemy in self.enemies:
            enemy.action(frametime, self.camera.position)
            if enemy.idlea <= 0:
                self.projectiles_enemy.append(RevolverBullet(len(self.dynamic_bullet_enemy), enemy.pos, glm.normalize(self.camera.position - enemy.pos), 20))
                self.dynamic_bullet_enemy.append(self.load_scene("bullet_02/bullet_02.gltf"))
                enemy.idlea = randint(2, 6)
            else:
                enemy.idlea -= 1 * frametime

            for node in self.dynamic_enemy[enemy.model_id].nodes:
                node._matrix_global = glm.translate(enemy.pos)

        # Position für Gegner-Projektile aktualisieren
        for projectile in self.projectiles_enemy:
            projectile.pos += projectile.v * frametime

            # Model-Matrix aktualisieren, wenn Distanz zu 0, 0, 0 > 500 löschen
            if glm.distance(glm.vec3(0, 0, 0), projectile.pos) < 500:

                for node in self.dynamic_bullet_enemy[projectile.model_id].nodes:
                    node._matrix_global = glm.translate(projectile.pos)

            else:
                self.id = projectile.model_id
                for projectile in self.projectiles_enemy:
                    if self.id < projectile.model_id:
                        projectile.model_id -= 1
                del self.dynamic_bullet_enemy[projectile.model_id]
                del self.projectiles_enemy[projectile.model_id]

        # Das gleiche für Spieler
        for projectile in self.projectiles_player:
            projectile.pos += projectile.v * frametime

            if glm.distance(glm.vec3(0, 0, 0), projectile.pos) < 500:

                for node in self.dynamic_bullet_player[projectile.model_id].nodes:
                    node._matrix_global = glm.translate(projectile.pos)

            else:
                self.id = projectile.model_id
                for projectile in self.projectiles_player:
                    if self.id < projectile.model_id:
                        projectile.model_id -= 1
                del self.dynamic_bullet_player[projectile.model_id]
                del self.projectiles_player[projectile.model_id]
            
        
        super().on_render(time, frametime)
    
# run
glw.run_window_config(DootWindow)
