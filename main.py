from moderngl_window.resources import programs
from moderngl_window.scene.programs import MeshProgram
from renderer.window import CollisionWindow, RenderWindow
import glm
import moderngl_window as glw
from moderngl_window.meta import ProgramDescription
import moderngl
from Projectile import *
from Enemy import *

class DootWindow(CollisionWindow):
    title = "DOOT"
    resource_dir = "assets"
    fullscreen = False
    vsync = False
    
    def __init__(self, **kwargs):        
        super().__init__("test/test.gltf", [["BarramundiFish/BarramundiFish.gltf"], [], []], **kwargs)
        self.camera.set_position(0.0, 0.0, 5.0)
        self.camera.velocity = 1.0
        self.jump_vel = 0.0
        self.enemies = [Plop(0, glm.vec3(10, 0, 10))]
        self.projectiles_enemy = []
        self.projectiles_player = []


    def on_render(self, time, frametime):
        #for node in self.dynamic[0].nodes:
        #    node._matrix_global = node._matrix_global * glm.translate(glm.vec3(0, 0, 0.001))
        
        for enemy in self.enemies:
            enemy.action(frametime, self.camera.position)
            if enemy.idlea <= 0:
                self.projectiles_enemy.append(RevolverBullet(len(self.dynamic_bullet_enemy), enemy.pos, self.camera.position, "player"))
                self.dynamic_bullet_enemy.append(self.load_scene("test/cube_entity.gltf"))
                enemy.idlea = random.randint(2, 6)
            else:
                enemy.idlea -= 1 * frametime

            for node in self.dynamic_enemy[enemy.model_id].nodes:
                node._matrix_global = glm.translate(enemy.pos)

        for projectile in self.projectiles_enemy:
            projectile.pos += projectile.v * frametime

            if glm.distance(glm.vec3(0, 0, 0), projectile.pos) < 50:

                for node in self.dynamic_bullet_enemy[projectile.model_id].nodes:
                    node._matrix_global = glm.translate(projectile.pos)

            else:
                del self.dynamic_bullet_enemy[projectile.model_id]
                del self.projectiles_enemy[projectile.model_id]
                for projectile in self.projectiles_enemy:
                    projectile.model_id -= 1
        
        for projectile in self.projectiles_player:
            projectile.pos += projectile.v * frametime

            if glm.distance(glm.vec3(0, 0, 0), projectile.pos) < 50:

                for node in self.dynamic_bullet_player[projectile.model_id].nodes:
                    node._matrix_global = glm.translate(projectile.pos)

            else:
                del self.dynamic_bullet_player[projectile.model_id]
                del self.projectiles_player[projectile.model_id]
                for projectile in self.projectiles_player:
                    projectile.model_id -= 1
            
        
        super().on_render(time, frametime)
    
                        
glw.run_window_config(DootWindow)
