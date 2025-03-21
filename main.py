from moderngl_window.resources import programs
from moderngl_window.scene.programs import MeshProgram
from renderer.window import CollisionWindow, RenderWindow
import glm
import moderngl_window as glw
from moderngl_window.meta import ProgramDescription
import moderngl
from Projectile import *
from Enemy import *
from Weapon import *
import subprocess
from random import randint

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


    def on_render(self, time, frametime):
        #for node in self.dynamic[0].nodes:
        #    node._matrix_global = node._matrix_global * glm.translate(glm.vec3(0, 0, 0.001))

        if time - self.enemy_last_time >= self.enemy_time:
            self.spawn_enemy = True
            self.enemy_last_time = time

        if self.mouse_pressed:
            self.weapon.shooting(self.camera.dir, self.camera.position, self.projectiles_player)
            self.dynamic_bullet_player.append(self.load_scene("bullet_01/bullet_01.gltf"))
            self.mouse_pressed = False



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
            if self.player_hp < 0:
                print("game over!")
                exit()

        if self.spawn_enemy:
            self.enemies.append(Plop(len(self.dynamic_enemy), glm.vec3(randint(-50, 50), randint(0, 3), randint(-50, 50))))
            self.dynamic_enemy.append(self.load_scene("Enemy/enemy.gltf"))
            self.spawn_enemy = False

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

            if self.enemies[enemy_id].hp < 1:
                for enemy in self.enemies:
                    if enemy_id < enemy.model_id:
                        enemy.model_id -= 1
                del self.dynamic_enemy[enemy_id]
                del self.enemies[enemy_id]


        for enemy in self.enemies:
            enemy.action(frametime, self.camera.position)
            if enemy.idlea <= 0:
                self.projectiles_enemy.append(RevolverBullet(len(self.dynamic_bullet_enemy), enemy.pos, glm.normalize(self.camera.position - enemy.pos), 20))
                self.dynamic_bullet_enemy.append(self.load_scene("bullet_02/bullet_02.gltf"))
                enemy.idlea = random.randint(2, 6)
            else:
                enemy.idlea -= 1 * frametime

            for node in self.dynamic_enemy[enemy.model_id].nodes:
                node._matrix_global = glm.translate(enemy.pos)


        for projectile in self.projectiles_enemy:
            projectile.pos += projectile.v * frametime

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
    
                        
glw.run_window_config(DootWindow)
