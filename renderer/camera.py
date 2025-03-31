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

    # Position aktualisieren
    def update_pos(self):
        now = time.time()
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

    # für Collision-Detection. Gibt die Nächste Position aus, tut aber nichts
    def get_update_pos(self, jump_vel):
        now = time.time()
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

        return pos

    # Gibt die View-Matrix
    @property
    def matrix(self) -> glm.mat4:
        return self._gl_look_at(self.position, self.position + self.dir, self._up)
