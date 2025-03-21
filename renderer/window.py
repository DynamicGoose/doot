import glm
import moderngl_window as glw
from renderer.camera import CollisionCamera
from moderngl_window import geometry
from moderngl_window.context.base import BaseKeys
import moderngl
import math
import fcl
import numpy as np

class CameraWindow(glw.WindowConfig):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = CollisionCamera(
            self.wnd.keys,
            fov=70.0,
            aspect_ratio=self.wnd.aspect_ratio,
            near=0.1,
            far=1000.0,
        )
        self.camera.velocity = 10.0
        self.camera.mouse_sensitivity = 0.25
        self.camera_enabled = True
        self.jump_vel = 0.0
        self.jump = False

    def on_key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if self.camera_enabled:
            self.camera.key_input(key, action, modifiers)
            self.wnd.mouse_exclusivity = True
            self.wnd.cursor = False
            
        # if action == keys.ACTION_PRESS:
        #     if key == keys.C:
        #         self.camera_enabled = not self.camera_enabled
        #         self.wnd.mouse_exclusivity = self.camera_enabled
        #         self.wnd.cursor = not self.camera_enabled
            # if key == keys.SPACE:
            #     self.timer.toggle_pause()


        if key == keys.SPACE and action == keys.ACTION_PRESS:
            self.jump = True

        if key == keys.SPACE and action == keys.ACTION_RELEASE:
            self.jump = False

        if key == keys.R and action == keys.ACTION_PRESS:
            self.spawn_enemy = True

    def on_mouse_position_event(self, x: int, y: int, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(-dx, -dy)

    def on_resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

    def on_mouse_press_event(self, x, y, button):
        if button == 1:
            self.mouse_pressed = True

    # def on_mouse_scroll_event(self, x_offset: float, y_offset: float) -> None:
    #     velocity = self.camera.velocity + y_offset
    #     self.camera.velocity = max(velocity, 1.0)

class RenderWindow(CameraWindow):
    resource_dir = "assets"

    def __init__(self, scene: str, dynamic: str, **kwargs):
        super().__init__(**kwargs)

        # Offscreen buffer
        offscreen_size = 4096, 4096
        self.offscreen_depth = self.ctx.depth_texture(offscreen_size)
        self.offscreen_depth.compare_func = ""
        self.offscreen_depth.repeat_x = False
        self.offscreen_depth.repeat_y = False
        # Less ugly by default with linear. May need to be NEAREST for some techniques
        self.offscreen_depth.filter = moderngl.LINEAR, moderngl.LINEAR

        self.offscreen = self.ctx.framebuffer(
            depth_attachment=self.offscreen_depth,
        )

        self.scene = self.load_scene(scene)
        self.dynamic = []
        self.dynamic_enemy = []
        self.dynamic_bullet_enemy = []
        self.dynamic_bullet_player = []

        for enemy in dynamic[0]:
            self.dynamic_enemy.append(self.load_scene(enemy))
        self.dynamic.append(self.dynamic_enemy)

        for bullet in dynamic[1]:
            self.dynamic_bullet_player.append(self.load_scene(bullet))
        self.dynamic.append(self.dynamic_bullet_player)
        
        for bullet in dynamic[2]:
            self.dynamic_bullet_enemy.append(self.load_scene(bullet))
        self.dynamic.append(self.dynamic_bullet_enemy)

        # Scene geometry
        self.sun = geometry.sphere(radius=1.0)

        # Programs
        self.basic_light = self.load_program("programs/shadow_mapping/directional_light.glsl")
        self.basic_light["shadowMap"].value = 0
        self.shadowmap_program = self.load_program("programs/shadow_mapping/shadowmap.glsl")
        self.sun_prog = self.load_program("programs/sun_debug.glsl")
        self.sun_prog["color"].value = 1, 1, 0, 1
        self.lightpos = 0, 0, 0

    def on_render(self, time, frametime):
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.lightpos = glm.vec3(math.sin(time * 0.1) * 10, 20, math.cos(time * 0.1) * 10)
        # self.lightpos = glm.vec3(10, 20, 10)

        # pass 1: render shadow map
        self.offscreen.clear()
        self.offscreen.use()

        depth_projection = glm.ortho(-40.0, 40.0, -40.0, 40.0, 1, 150.0)
        depth_view = glm.lookAt(self.lightpos, (0, 0, 0), (0, 1, 0))
        depth_mvp = depth_projection * depth_view
        self.shadowmap_program["mvp"].write(depth_mvp)

        for node in self.scene.nodes:
            self.draw_nodes_depth(node)

        for array in self.dynamic:
            for entity in array:
                for node in entity.nodes:
                    self.draw_nodes_depth(node)

        # pass 2: render scene
        self.wnd.use()
        self.basic_light["m_proj"].write(self.camera.projection.matrix)
        self.basic_light["m_camera"].write(self.camera.matrix)
        self.basic_light["mvp"].write(depth_mvp)
        self.basic_light["lightPos"].write(self.lightpos)
        self.basic_light["viewPos"].write(self.camera.position)
        self.offscreen_depth.use(location=0)

        for node in self.scene.nodes:
            self.draw_nodes_light(node)

        for array in self.dynamic:
            for entity in array:
                for node in entity.nodes:
                    self.draw_nodes_light(node)
                        
        # Render the sun position
        self.sun_prog["m_proj"].write(self.camera.projection.matrix)
        self.sun_prog["m_camera"].write(self.camera.matrix)
        self.sun_prog["m_model"].write(glm.translate(glm.vec3(self.lightpos)))
        self.sun.render(self.sun_prog)

    def draw_nodes_light(self, node):
        if node.mesh:
            self.basic_light["m_model"].write(node.matrix_global)
            node.mesh.material.mat_texture.texture.use(location=1)
            self.basic_light["texture1"].value = 1
            node.mesh.vao.render(self.basic_light)
        for child in node.children:
            self.draw_nodes_light(child)

    def draw_nodes_depth(self, node):
        if node.mesh:
            self.shadowmap_program["m_model"].write(node.matrix_global)
            node.mesh.vao.render(self.shadowmap_program)
        for child in node.children:
            self.draw_nodes_depth(child)

class CollisionWindow(RenderWindow):
    def __init__(self, scene: str, dynamic: str, **kwargs):
        super().__init__(scene, dynamic, **kwargs)
        
        collisionObjects = []
        for node in self.scene.nodes:
            collisionObjects += self.get_collision_objects(node, [])
        self.collisionManager = fcl.DynamicAABBTreeCollisionManager()
        self.collisionManager.registerObjects(collisionObjects)
        self.collisionManager.setup()

        self.entityCollisions = []
        self.enemyProjectiles = fcl.DynamicAABBTreeCollisionManager()
        self.playerProjectiles = fcl.DynamicAABBTreeCollisionManager()

        # entityCollisionObjects = []
        # for entity in self.dynamic:
        #     for node in entity.nodes:
        #         entityCollisionObjects += self.get_collision_objects(node, [])
        # self.entityCollisionManager = fcl.DynamicAABBTreeCollisionManager()
        # self.entityCollisionManager.registerObjects(entityCollisionObjects)
        # self.entityCollisionManager.setup()
        # print(self.entityCollisionManager.getObjects())

        camColMesh = fcl.Capsule(0.1, 1.0)
        camTransform = fcl.Transform(np.array(self.camera.position - glm.vec3(0.0, 0.5, 0.0)))
        self.cameraCollisionObject = fcl.CollisionObject(camColMesh, camTransform)
        
        self.colliding = False
        
    def on_render(self, time, frametime):

        # entity hitboxes
        entityCollisionObjects = []
        for entity in self.dynamic[0]:
            for node in entity.nodes:
                entityCollisionObjects += self.get_collision_objects(node, [])
        self.entityCollisions = entityCollisionObjects

        # player projectiles
        playerProjectiles = []
        for entity in self.dynamic[1]:
            for node in entity.nodes:
                playerProjectiles += self.get_collision_objects(node, [])
        self.playerProjectiles.clear()
        self.playerProjectiles.registerObjects(playerProjectiles)
        self.playerProjectiles.setup()

        # enemy projectiles
        enemyProjectiles = []
        for entity in self.dynamic[2]:
            for node in entity.nodes:
                enemyProjectiles += self.get_collision_objects(node, [])
        self.enemyProjectiles.clear()
        self.enemyProjectiles.registerObjects(enemyProjectiles)
        self.enemyProjectiles.setup()
        
        if self.jump_vel == 0.0 and self.jump == True:
            self.jump_vel = 7
        self.camera.position.y += self.jump_vel * frametime
        if self.detect_cam_collision():
            self.jump_vel = 0.0
        elif self.camera.position[1] > 0.01 and not self.detect_cam_collision():
            self.jump_vel -= 15 * frametime
        else:
            self.camera.position[1] = 0.00
            self.jump_vel = 0.0

        next_pos = self.camera.get_update_pos(self.jump_vel)
    
        self.cameraCollisionObject.setTranslation(np.array(next_pos - glm.vec3(0.0, 0.5, 0.0)))
        
        if self.detect_cam_collision():
            self.camera._last_time = self.camera._check_last_time
            self.camera.position += (self.camera.position - glm.vec3(self.detect_cam_distance().nearest_points[1])) * 0.1
        # elif self.detect_cam_entity_collision():
        #     self.camera._last_time = self.camera._check_last_time
        #     self.camera.position += (self.camera.position - glm.vec3(self.detect_cam_entity_distance().nearest_points[1])) * 0.1
        else:
            self.camera.update_pos()
            
        super().on_render(time, frametime)

        # # Draw bounding boxes
        # self.scene.draw_bbox(
        #     projection_matrix=self.camera.projection.matrix,
        #     camera_matrix=self.camera.matrix,
        #     children=True,
        #     color=(0.75, 0.75, 0.75),
        # )

        # for entity in self.dynamic:
        #     entity.draw_bbox(
        #         projection_matrix=self.camera.projection.matrix,
        #         camera_matrix=self.camera.matrix,
        #         children=True,
        #         color=(0.75, 0.75, 0.75),
        #     )

    def get_collision_objects(self, node: glw.scene.Node, collisionObjects):
        if node.mesh:
            m = fcl.Box(
                (node.mesh.bbox_max[0] - node.mesh.bbox_min[0]) * 0.5,
                (node.mesh.bbox_max[1] - node.mesh.bbox_min[1]) * 0.5,
                (node.mesh.bbox_max[2] - node.mesh.bbox_min[2]) * 0.5,
            )
            t = fcl.Transform(np.array(glm.mat3(node.matrix_global)), np.array(glm.vec3(node.matrix_global[3])))
            collisionObjects.append(fcl.CollisionObject(m, t))
        for child in node.children:
            collisionObjects += self.get_collision_objects(child, [])

        return collisionObjects

    def detect_cam_distance(self):
        req = fcl.DistanceRequest(enable_nearest_points=False, enable_signed_distance=True)
        rdata = fcl.DistanceData(request=req)

        self.collisionManager.distance(self.cameraCollisionObject, rdata, fcl.defaultDistanceCallback)

        return rdata.result

    def detect_cam_collision(self):
        req = fcl.CollisionRequest()
        rdata = fcl.CollisionData(request=req)

        self.collisionManager.collide(self.cameraCollisionObject, rdata, fcl.defaultCollisionCallback)

        return rdata.result.is_collision
        
    def detect_player_hit(self):
        req = fcl.CollisionRequest()
        rdata = fcl.CollisionData(request=req)

        self.enemyProjectiles.collide(self.cameraCollisionObject, rdata, fcl.defaultCollisionCallback)

        return rdata.result.is_collision

    def detect_enemy_hits(self):
        collisions = []
        for i, collisionObject in enumerate(self.entityCollisions):
            req = fcl.CollisionRequest()
            rdata = fcl.CollisionData(request=req)
            self.playerProjectiles.collide(collisionObject, rdata, fcl.defaultCollisionCallback)
            if rdata.result.is_collision:
                collisions.append(i)

        return collisions
