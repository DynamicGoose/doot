from moderngl_window.scene import KeyboardCamera
from moderngl_window.utils.keymaps import QWERTY, KeyMapFactory
from moderngl_window.context.base import BaseKeys
import time
import glm
import copy

class CollisionCamera(KeyboardCamera):
    def __init__(
        self,
        keys: BaseKeys,
        keymap: KeyMapFactory = QWERTY,
        fov: float = 60.0,
        aspect_ratio: float = 1.0,
        near: float = 1.0,
        far: float = 100.0,
    ):
        super().__init__(keys, keymap, fov, aspect_ratio, near, far)
        self.r = 1

        self._check_last_time = time.time()
    
    def update_pos(self):
        # Use separate time in camera so we can move it when the demo is paused
        now = time.time()
        # If the camera has been inactive for a while, a large time delta
        # can suddenly move the camera far away from the scene
        t = max(now - self._last_time, 0)
        self._last_time = now

        # X Movement
        self.r = copy.copy(self.right)
        self.r[1] = 0
        self.r = glm.normalize(self.r)
        if self._xdir == 1:
            self.position += self.r * self._velocity * t
        elif self._xdir == 2:
            self.position -=  self.r * self._velocity * t

        # Z Movement
        self.d = copy.copy(self.dir)
        self.d[1] = 0
        self.d = glm.normalize(self.d)
        if self._zdir == 2:
            self.position += self.d * self._velocity * t
        elif self._zdir == 1:
            self.position -= self.d * self._velocity * t
        
        # pos = self.position + self.jump_vel * t
        # # Y Movement
        # if self._ydir == 1:
        #     self.position += self.up * self._velocity * t
        # elif self._ydir == 2:
        #     self.position -= self.up * self._velocity * t

    def get_update_pos(self, jump_vel):
        # Use separate time in camera so we can move it when the demo is paused
        now = time.time()
        # If the camera has been inactive for a while, a large time delta
        # can suddenly move the camera far away from the scene
        t = max(now - self._check_last_time, 0)
        self._check_last_time = now
        
        pos = glm.vec3(0)
        
        # X Movement
        if self._xdir == 1:
            pos = self.position + self.right * self._velocity * t
        elif self._xdir == 2:
            pos = self.position - self.right * self._velocity * t
        
        # Z Movement
        self.d = 1
        if self._zdir == 2:
            pos = self.position + self.dir * self._velocity * t
        elif self._zdir == 1:
            pos = self.position - self.dir * self._velocity * t

        pos = self.position + jump_vel * t

        # Y Movement
        # if self._ydir == 1:
        #     pos = self.position + self.up * self._velocity * t
        # elif self._ydir == 2:
        #     pos = self.position - self.up * self._velocity * t

        return pos
        
    @property
    def matrix(self) -> glm.mat4:
        return self._gl_look_at(self.position, self.position + self.dir, self._up)
