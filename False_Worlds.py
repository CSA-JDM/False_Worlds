# Jacob Meadows
# Practicum IT, 7th - 8th Periods
# 23 November, 2019
"""
False Worlds: Jacob Meadows' final program for Practicum IT
    Copyright (C) 2019  Jacob Meadows

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import glfw
import numpy
import pyrr
import noise
import os
import random
from PIL import Image
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class App:
    def __init__(self, width, height, title):
        # region GLFW Initialization
        if not glfw.init():
            raise Exception("GLFW can not be initialized!")

        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can not be created!")

        glfw.set_window_pos(self.window, 400, 200)
        glfw.set_window_size_callback(self.window, self.window_resize)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.make_context_current(self.window)
        # endregion

        shader = compileProgram(compileShader(open("vertex.glsl", "r").read(), GL_VERTEX_SHADER),
                                compileShader(open("fragment.glsl", "r").read(), GL_FRAGMENT_SHADER))
        self.projection_loc = glGetUniformLocation(shader, "projection")
        self.projection_3d = pyrr.matrix44.create_perspective_projection_matrix(90, 1280 / 720, 0.1, 100.0)
        self.projection_2d = pyrr.matrix44.create_orthogonal_projection_matrix(0, 1280, 720, 0, 0.01, 100.0)
        self.view_loc = glGetUniformLocation(shader, "view")
        view_2d = pyrr.matrix44.create_from_translation([0.0, 0.0, 0.0])

        glClearColor(135 / 255, 206 / 255, 235 / 255, 1.0)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.keys = [False] * 1024
        self.width, self.height = width, height
        self.mouse_visibility = False
        self.in_inventory = False
        self.paused = False
        self.fps = 0
        self.time_p = glfw.get_timer_value()
        self.player = Camera()
        self.grass_block = Block(None)
        positions = numpy.array([], dtype=numpy.float32)
        for x in range(-60, 60):
            for y in range(-60, 60):
                if len(positions) > 0:
                    positions = numpy.append(positions, numpy.array([numpy.dot(pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5]), pyrr.matrix44.create_from_translation([x, y, -1.0]))], dtype=numpy.float32), 0)
                else:
                    positions = numpy.array([numpy.dot(pyrr.matrix44.create_from_scale([0.5, 0.5, 0.5]), pyrr.matrix44.create_from_translation([x, y, -1.0]))], dtype=numpy.float32)
        entity_positions = numpy.array([], dtype=numpy.float32)
        for x in range(-10, 10):
            x /= 2
            for z in range(-10, 10):
                z /= 2
                if len(entity_positions) > 0:
                    entity_positions = numpy.append(entity_positions, numpy.array([numpy.dot(pyrr.matrix44.create_from_scale([0.25, 0.25, 0.25]), pyrr.matrix44.create_from_translation([x, -1, z]))], dtype=numpy.float32), 0)
                else:
                    entity_positions = numpy.array([numpy.dot(pyrr.matrix44.create_from_scale([0.25, 0.25, 0.25]), pyrr.matrix44.create_from_translation([x, -1, z]))], dtype=numpy.float32)
        for side in self.grass_block.sides:
            side.transform_update(numpy.append(positions, entity_positions, 0))

        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            old_fps = self.fps
            time_n = glfw.get_timer_value()
            time_s = (time_n - self.time_p) / 10000000
            self.time_p = time_n
            self.fps = round(time_s ** -1)
            print(self.fps)

            for entity_position in range(len(entity_positions)):
                entity_positions[entity_position] = numpy.dot(pyrr.matrix44.create_from_y_rotation(0.01), entity_positions[entity_position])
            for side in self.grass_block.sides:
                side.transform_update(numpy.append(positions, entity_positions, 0))
            self.do_movement(time_s)
            glUseProgram(shader)
            view = self.player.get_view_matrix()
            glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, self.projection_3d)
            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view)

            for side in self.grass_block.sides:
                glBindVertexArray(side.vao)
                glBindTexture(GL_TEXTURE_2D, side.texture)
                glDrawElementsInstanced(GL_TRIANGLES, len(side.index), GL_UNSIGNED_INT, None, int(len(side.transform)))
                glBindTexture(GL_TEXTURE_2D, 0)
                glBindVertexArray(0)

            glfw.swap_buffers(self.window)

        glfw.terminate()

    def do_movement(self, time_s):
        net_movement = 4.317 * time_s
        if self.keys[glfw.KEY_W]:
            if self.player.sprint_delay > 0 and not self.player.holding_walk:
                self.player.sprinting = True
            elif self.player.sprint_delay == 0 and not self.player.holding_walk:
                self.player.sprint_delay = 0.25
            self.player.holding_walk = True
            if self.player.flying:
                if self.player.sprinting:
                    self.player.process_keyboard("FRONT", net_movement * 5.0)
                else:
                    self.player.process_keyboard("FRONT", net_movement * 2.5)
            elif self.player.crouching:
                self.player.process_keyboard("FRONT", net_movement * 0.3)
            else:
                if self.player.sprinting:
                    self.player.process_keyboard("FRONT", net_movement * 1.3)
                else:
                    self.player.process_keyboard("FRONT", net_movement)
        else:
            self.player.holding_walk = False
            self.player.sprinting = False
        if self.keys[glfw.KEY_A]:
            if self.player.flying:
                self.player.process_keyboard("SIDE", -net_movement * 2.5)
            elif self.player.crouching:
                self.player.process_keyboard("SIDE", -net_movement * 0.3)
            else:
                self.player.process_keyboard("SIDE", -net_movement)
        if self.keys[glfw.KEY_S]:
            if self.player.flying:
                self.player.process_keyboard("FRONT", -net_movement * 2.5)
            elif self.player.crouching:
                self.player.process_keyboard("FRONT", -net_movement * 0.3)
            else:
                self.player.process_keyboard("FRONT", -net_movement)
        if self.keys[glfw.KEY_D]:
            if self.player.flying:
                self.player.process_keyboard("SIDE", net_movement * 2.5)
            elif self.player.crouching:
                self.player.process_keyboard("SIDE", net_movement * 0.3)
            else:
                self.player.process_keyboard("SIDE", net_movement)

    def mouse_callback(self, window, dx, dy):
        if not self.mouse_visibility:
            x_offset = dx - self.width / 2
            y_offset = self.height / 2 - dy
            self.player.process_mouse_movement(x_offset, y_offset)
            glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2)

    def scroll_callback(self, window, dx, dy):
        pass

    def mouse_button_callback(self, window, button, action, mods):
        pass

    def key_callback(self, window, key, scancode, action, mode):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            if not self.mouse_visibility:
                glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)
                self.mouse_visibility = True
            elif self.in_inventory:
                glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2)
                glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
                self.mouse_visibility = False
                self.in_inventory = False
                self.paused = False
            else:
                glfw.set_window_should_close(self.window, True)
        if 0 <= key < 1024:
            if action == glfw.PRESS:
                self.keys[key] = True
            elif action == glfw.RELEASE:
                self.keys[key] = False

    def window_resize(self, window, width, height):
        glViewport(0, 0, width, height)
        self.projection_3d = pyrr.matrix44.create_perspective_projection_matrix(90, width / height, 0.1, 100.0)
        self.projection_2d = pyrr.matrix44.create_orthogonal_projection_matrix(0, width, height, 0, 0.01, 100.0)
        self.width, self.height = width, height


class Camera:
    def __init__(self):
        self.pos = pyrr.Vector3([0.0, 0.0, 0.0])
        self.front = pyrr.Vector3([0.0, 0.0, -1.0])
        self.up = pyrr.Vector3([0.0, 1.0, 0.0])
        self.right = pyrr.Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.125
        self.yaw = -90.0
        self.pitch = 0.0

        self.jumping = False
        self.crouching = False
        self.holding_walk = False
        self.holding_jump = False
        self.sprinting = False
        self.flying = False
        self.placing = False
        self.breaking = False
        self.sprint_delay = 0
        self.place_delay = 0
        self.break_delay = 0
        self.fly_delay = 0
        self.air_vel = 0
        self.inventory = [None] * 27
        self.hotbar = [None] * 9

    def get_view_matrix(self):
        return self.look_at(self.pos, self.pos + self.front, self.up)

    def process_keyboard(self, direction, velocity):
        if direction == "FRONT":
            self.pos.x += numpy.cos(numpy.radians(self.yaw)) * velocity
            # self.app.check_pos(0, numpy.cos(numpy.radians(self.yaw)) * velocity)
            self.pos.z += numpy.sin(numpy.radians(self.yaw)) * velocity
            # self.app.check_pos(2, numpy.sin(numpy.radians(self.yaw)) * velocity)
        elif direction == "SIDE":
            self.pos.x += numpy.cos(numpy.radians(self.yaw) + numpy.pi / 2) * velocity
            # self.app.check_pos(0, numpy.cos(numpy.radians(self.yaw) + numpy.pi / 2) * velocity)
            self.pos.z += numpy.sin(numpy.radians(self.yaw) + numpy.pi / 2) * velocity
            # self.app.check_pos(2, numpy.sin(numpy.radians(self.yaw) + numpy.pi / 2) * velocity)
        elif direction == "UP":
            self.pos.y += velocity

    def process_mouse_movement(self, x_offset, y_offset, constrain_pitch=True):
        x_offset *= self.mouse_sensitivity
        y_offset *= self.mouse_sensitivity

        self.yaw += x_offset
        self.pitch += y_offset

        if constrain_pitch:
            if self.pitch > 90.0:
                self.pitch = 90.0
            if self.pitch < -90.0:
                self.pitch = -90.0

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = pyrr.Vector3([0.0, 0.0, 0.0])
        front.x = numpy.cos(numpy.radians(self.yaw)) * numpy.cos(numpy.radians(self.pitch))
        front.y = numpy.sin(numpy.radians(self.pitch))
        front.z = numpy.sin(numpy.radians(self.yaw)) * numpy.cos(numpy.radians(self.pitch))

        self.front = pyrr.vector.normalise(front)
        self.right = pyrr.vector.normalise(pyrr.vector3.cross(self.front, pyrr.Vector3([0.0, 1.0, 0.0])))
        self.up = pyrr.vector.normalise(pyrr.vector3.cross(self.right, self.front))

    @staticmethod
    def look_at(position, target, world_up):
        z_axis = pyrr.vector.normalise(position - target)
        x_axis = pyrr.vector.normalise(pyrr.vector3.cross(pyrr.vector.normalise(world_up), z_axis))
        y_axis = pyrr.vector3.cross(z_axis, x_axis)

        translation = pyrr.Matrix44.identity()
        translation[3][0] = -position.x
        translation[3][1] = -position.y
        translation[3][2] = -position.z

        rotation = pyrr.Matrix44.identity()
        rotation[0][0] = x_axis[0]
        rotation[1][0] = x_axis[1]
        rotation[2][0] = x_axis[2]
        rotation[0][1] = y_axis[0]
        rotation[1][1] = y_axis[1]
        rotation[2][1] = y_axis[2]
        rotation[0][2] = z_axis[0]
        rotation[1][2] = z_axis[1]
        rotation[2][2] = z_axis[2]

        return rotation * translation


class Entity:
    def __init__(self, vertex, index, texture, transpose=False):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vertex_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 5, ctypes.c_void_p(0))

        self.index_ebo = glGenBuffers(1)
        self.index = index
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, index.nbytes, index, GL_STATIC_DRAW)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertex.itemsize * 5, ctypes.c_void_p(12))
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        self.transform_vbo = glGenBuffers(1)
        self.transform = None

        self.texture = self.load_texture(texture, transpose)

        glBindVertexArray(0)

    def transform_update(self, transform):
        glBindVertexArray(self.vao)
        self.transform = transform
        glBindBuffer(GL_ARRAY_BUFFER, self.transform_vbo)
        glBufferData(GL_ARRAY_BUFFER, transform.nbytes, transform.flatten(), GL_STATIC_DRAW)
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, transform.flatten().itemsize * 16, ctypes.c_void_p(0))
        glVertexAttribDivisor(2, 1)
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, transform.flatten().itemsize * 16, ctypes.c_void_p(16))
        glVertexAttribDivisor(3, 1)
        glEnableVertexAttribArray(4)
        glVertexAttribPointer(4, 4, GL_FLOAT, GL_FALSE, transform.flatten().itemsize * 16, ctypes.c_void_p(32))
        glVertexAttribDivisor(4, 1)
        glEnableVertexAttribArray(5)
        glVertexAttribPointer(5, 4, GL_FLOAT, GL_FALSE, transform.flatten().itemsize * 16, ctypes.c_void_p(48))
        glVertexAttribDivisor(5, 1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    @staticmethod
    def load_texture(texture_file, transpose=False):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        if isinstance(texture_file, str):
            image = Image.open(texture_file)
            if transpose:
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            width, height = image.width, image.height
            img_data = numpy.array(list(image.getdata()), numpy.uint8)
        else:
            cx, cy = texture_file[1]
            image = texture_file[0]
            orig_data = numpy.array(list(image.getdata()), numpy.uint8).reshape((image.height, image.width * 4))
            img_data = numpy.empty((8, texture_file[2][0] * 4), dtype=numpy.uint8)
            for x in range(cx * 4, (cx + texture_file[2][0]) * 4):
                for y in range(cy, cy + 8):
                    img_data[y - cy, x - (cx * 4)] = orig_data[y, x]
            width, height = texture_file[2][0], 8
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glBindTexture(GL_TEXTURE_2D, 0)
        return texture


class Block:
    def __init__(self, textures):
        front_v = numpy.array([
            -0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0
        ], dtype=numpy.float32)
        back_v = numpy.array([
            0.5, -0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 1.0,
            0.5, 0.5, -0.5, 0.0, 1.0
        ], dtype=numpy.float32)
        right_v = numpy.array([
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 0.0, 1.0,
            0.5, -0.5, 0.5, 0.0, 0.0
        ], dtype=numpy.float32)
        left_v = numpy.array([
            -0.5, 0.5, -0.5, 0.0, 1.0,
            -0.5, -0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, 0.5, 1.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 1.0,
        ], dtype=numpy.float32)
        bottom_v = numpy.array([
            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 1.0,
        ], dtype=numpy.float32)
        top_v = numpy.array([
            0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 0.0, 1.0
        ], dtype=numpy.float32)
        index_data = numpy.array([0, 1, 2, 2, 3, 0], dtype=numpy.uint32)
        self.front = Entity(front_v, index_data, "textures/grass.png", transpose=True)
        self.back = Entity(back_v, index_data, "textures/grass.png", transpose=True)
        self.right = Entity(right_v, index_data, "textures/grass.png", transpose=True)
        self.left = Entity(left_v, index_data, "textures/grass.png", transpose=True)
        self.bottom = Entity(bottom_v, index_data, "textures/dirt.png", transpose=True)
        self.top = Entity(top_v, index_data, "textures/grass_top.png", transpose=True)
        self.sides = [self.front, self.back, self.right, self.left, self.top, self.bottom]


if __name__ == '__main__':
    App(1280, 720, "False Worlds")
