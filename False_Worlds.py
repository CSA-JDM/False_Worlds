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
from PIL import Image
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


HIGHLIGHTED_CUBE = numpy.array([-0.02, -0.02, 1.02, 0.0, 0.0,
                                1.02, -0.02, 1.02, 1.0, 0.0,
                                1.02, 1.02, 1.02, 1.0, 1.0,
                                -0.02, 1.02, 1.02, 0.0, 1.0,

                                -0.02, -0.02, -0.02, 0.0, 0.0,
                                1.02, -0.02, -0.02, 1.0, 0.0,
                                1.02, 1.02, -0.02, 1.0, 1.0,
                                -0.02, 1.02, -0.02, 0.0, 1.0,

                                1.02, -0.02, -0.02, 0.0, 0.0,
                                1.02, 1.02, -0.02, 0.0, 1.0,
                                1.02, 1.02, 1.02, 1.0, 1.0,
                                1.02, -0.02, 1.02, 1.0, 0.0,

                                -0.02, 1.02, -0.02, 1.0, 1.0,
                                -0.02, -0.02, -0.02, 1.0, 0.0,
                                -0.02, -0.02, 1.02, 0.0, 0.0,
                                -0.02, 1.02, 1.02, 0.0, 1.0,

                                -0.02, -0.02, -0.02, 0.0, 0.0,
                                1.02, -0.02, -0.02, 1.0, 0.0,
                                1.02, -0.02, 1.02, 1.0, 1.0,
                                -0.02, -0.02, 1.02, 0.0, 1.0,

                                1.02, 1.02, -0.02, 0.0, 0.0,
                                -0.02, 1.02, -0.02, 1.0, 0.0,
                                -0.02, 1.02, 1.02, 1.0, 1.0,
                                1.02, 1.02, 1.02, 0.0, 1.0], dtype=numpy.float32)
CUBE_INDICES_EDGES = numpy.array([0, 1, 2, 3,
                                  6, 5, 4, 7,
                                  8, 9, 10, 11,
                                  12, 13, 14, 15,
                                  16, 17, 18, 19,
                                  20, 21, 22, 23], dtype=numpy.uint32)
CHARACTER_DICT = {
    "a": (((8, 48), (5, 5)), ((8, 32), (5, 7))),
    "b": (((16, 48), (5, 7)), ((16, 32), (5, 7))),
    "c": (((24, 48), (5, 5)), ((24, 32), (5, 7))),
    "d": (((32, 48), (5, 7)), ((32, 32), (5, 7))),
    "e": (((40, 48), (5, 5)), ((40, 32), (5, 7))),
    "f": (((48, 48), (4, 7)), ((48, 32), (5, 7))),
    "g": (((56, 48), (5, 6)), ((56, 32), (5, 7))),
    "h": (((64, 48), (5, 7)), ((64, 32), (5, 7))),
    "i": (((72, 48), (1, 7)), ((72, 32), (3, 7))),
    "j": (((80, 48), (5, 8)), ((80, 32), (5, 7))),
    "k": (((88, 48), (4, 7)), ((88, 32), (5, 7))),
    "l": (((96, 48), (2, 7)), ((96, 32), (5, 7))),
    "m": (((104, 48), (5, 5)), ((104, 32), (5, 7))),
    "n": (((112, 48), (5, 5)), ((112, 32), (5, 7))),
    "o": (((120, 48), (5, 5)), ((120, 32), (5, 7))),
    "p": (((0, 56), (5, 6)), ((0, 40), (5, 7))),  # temporary capital size values (5, 7)
    "q": (((8, 56), (5, 6)), ((8, 40), (5, 7))),  # temporary capital size values (5, 7)
    "r": (((16, 56), (5, 5)), ((16, 40), (5, 7))),  # temporary capital size values (5, 7)
    "s": (((24, 56), (5, 5)), ((24, 40), (5, 7))),  # temporary capital size values (5, 7)
    "t": (((32, 56), (3, 7)), ((32, 40), (5, 7))),  # temporary capital size values (5, 7)
    "u": (((40, 56), (5, 5)), ((40, 40), (5, 7))),  # temporary capital size values (5, 7)
    "v": (((48, 56), (5, 5)), ((48, 40), (5, 7))),  # temporary capital size values (5, 7)
    "w": (((56, 56), (5, 5)), ((56, 40), (5, 7))),  # temporary capital size values (5, 7)
    "x": (((64, 56), (5, 5)), ((64, 40), (5, 7))),  # temporary capital size values (5, 7)
    "y": (((72, 56), (5, 6)), ((72, 40), (5, 7))),  # temporary capital size values (5, 7)
    "z": (((80, 56), (5, 5)), ((80, 40), (5, 7))),  # temporary capital size values (5, 7)
}
SPECIAL_CHARACTER_DICT = {
    ".": ((112, 16), (1, 2)),
    ">": ((112, 24), (4, 7)),
    ",": ((96, 16), (1, 3)),
    "<": ((96, 24), (4, 7)),
    "-": ((104, 16), (5, 1)),
    "*": ((80, 16), (4, 3)),
    ":": ((80, 24), (1, 6)),
    "0": ((0, 24), (5, 7)),
    "1": ((8, 24), (5, 7)),
    "2": ((16, 24), (5, 7)),
    "3": ((24, 24), (5, 7)),
    "4": ((32, 24), (5, 7)),
    "5": ((40, 24), (5, 7)),
    "6": ((48, 24), (5, 7)),
    "7": ((56, 24), (5, 7)),
    "8": ((64, 24), (5, 7)),
    "9": ((72, 24), (5, 7))
}
ASCII_PNG = Image.open("textures/ascii.png")


class App:
    def __init__(self, width, height, title, monitor=None, share=None):
        # region GLFW Initialization
        if not glfw.init():
            raise Exception("GLFW can not be initialized!")

        self.window = glfw.create_window(width, height, title, monitor, share)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window can not be created!")

        glfw.set_window_pos(self.window, 400, 200)
        glfw.set_window_size_callback(self.window, self.window_resize)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.make_context_current(self.window)
        # endregion

        # region Variables
        self.keys = [False] * 1024
        self.y_values = [[0 for _ in range(128)] for _ in range(128)]
        self.world = dict()
        self.mouse_visibility = True
        self.in_menu = True
        self.in_game = True
        self.in_inventory = False
        self.paused = False
        self.new_game = False
        self.highlighted = None
        self.breaking_block = None
        self.selected_block = "dirt"
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
        self.air_velocity = 0
        self.time_p = glfw.get_timer_value()
        shader = compileProgram(compileShader(open("vertex.glsl", "r").read(), GL_VERTEX_SHADER),
                                compileShader(open("fragment.glsl", "r").read(), GL_FRAGMENT_SHADER))
        self.projection_loc = glGetUniformLocation(shader, "projection")
        self.model_loc = glGetUniformLocation(shader, "model")
        self.view_loc = glGetUniformLocation(shader, "view")
        self.camera = Camera(self)
        self.vaos_3d = dict()
        self.vaos_2d = dict()
        block_break = list()
        # endregion

        self.vaos_3d["grass"] = Cube(["textures/grass_side.png"] * 2 + ["textures/blocks/dirt.png"] +
                                     ["textures/grass_top.png"] + ["textures/grass_side.png"] * 2)
        highlighted_vao = VAO("textures/black.png", HIGHLIGHTED_CUBE, CUBE_INDICES_EDGES)
        for block in os.listdir("./textures/blocks"):
            self.vaos_3d[block.split(".")[0]] = Cube([f"textures/blocks/{block}"] * 6)
        for stage in range(10):
            block_break.append(VAO.load_texture(f"textures/destroy_stage_{stage}.png"))
        glUseProgram(shader)
        glClearColor(135.0 / 255.0, 206.0 / 255.0, 235.0 / 255.0, 1.0)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLineWidth(4)  # todo figure out how large the outlines need to be for highlighted blocks
        projection = pyrr.matrix44.create_perspective_projection_matrix(90, 1280 / 720, 0.1, 100.0)
        translation = pyrr.matrix44.create_from_translation([0.0, -1.65, 0.0])
        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, translation)
        self.game_init()

        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            time_n = glfw.get_timer_value()
            time_s = (time_n - self.time_p) / 10000000
            self.time_p = time_n
            self.do_movement(time_s)
            self.mouse_button_check(time_s)
            view = self.camera.get_view_matrix()
            # region Highlighting
            mx, my = glfw.get_cursor_pos(self.window)
            ray_nds = pyrr.Vector3([(2.0 * mx) / 1280 - 1.0, 1.0 - (2.0 * my) / 720, 1.0])
            ray_clip = pyrr.Vector4([*ray_nds.xy, -1.0, 1.0])
            ray_eye = pyrr.Vector4(numpy.dot(numpy.linalg.inv(projection), ray_clip))
            ray_eye = pyrr.Vector4([*ray_eye.xy, -1.0, 0.0])
            ray_wor = (numpy.linalg.inv(view) * ray_eye).xyz
            self.ray_wor = pyrr.vector.normalise(ray_wor)
            for i in numpy.arange(1, 4, 0.01):
                ray_cam = self.camera.camera_pos + self.ray_wor * i
                ray_cam.y += 1.62
                self.ray_cam = ray_cam
                self.ray_i = i
                ray_cam.x, ray_cam.y, ray_cam.z = int(self.check_value(ray_cam.x, 0)), \
                    int(self.check_value(ray_cam.y, 0)), int(self.check_value(ray_cam.z, 0))
                ray_cam = [int(axis) for axis in ray_cam]
                if tuple(ray_cam) in self.world:
                    self.highlighted = numpy.array(ray_cam, dtype=numpy.float32)
                    break
            if self.highlighted is not None and list(self.highlighted) != ray_cam:
                self.highlighted = None
            # endregion
            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view)
            for cube in self.vaos_3d.values():
                for vao in cube.vaos.values():
                    glBindVertexArray(vao.vao)
                    if vao.instance_data is not None:
                        glBindTexture(GL_TEXTURE_2D, vao.texture)
                        glDrawElementsInstanced(
                            GL_TRIANGLES, len(vao.indices), GL_UNSIGNED_INT, None, int(len(vao.instance_data))
                        )
                        glBindTexture(GL_TEXTURE_2D, 0)
                    glBindVertexArray(0)
            if self.highlighted is not None:
                if not numpy.array_equal(self.highlighted, highlighted_vao.instance_data):
                    highlighted_vao.instance_update(self.highlighted)
                glBindVertexArray(highlighted_vao.vao)
                if self.breaking:
                    if self.break_delay >= 0:
                        glBindTexture(GL_TEXTURE_2D, block_break[
                            int(-(self.break_delay - (0.5 - (0.5 / 10))) / (0.5 / 10))
                        ])
                    else:
                        glBindTexture(GL_TEXTURE_2D, block_break[int((0.5 - (0.5 / 10)) / (0.5 / 10))])
                    glDrawElementsInstanced(GL_QUADS, len(highlighted_vao.indices), GL_UNSIGNED_INT, None,
                                            int(len(highlighted_vao.instance_data) / 3))
                    glBindTexture(GL_TEXTURE_2D, 0)
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                glDrawElementsInstanced(GL_QUADS, len(highlighted_vao.indices), GL_UNSIGNED_INT, None,
                                        int(len(highlighted_vao.instance_data) / 3))
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                glBindVertexArray(0)

            glfw.swap_buffers(self.window)

        glfw.terminate()

    def main_menu(self):
        pass

    def game_init(self):
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        self.mouse_visibility = False
        scale = 100.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        for i in range(128):
            for j in range(128):
                self.y_values[i][j] = int(noise.pnoise2(
                    i / scale, j / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity,
                    repeatx=128, repeaty=128, base=0
                ) * 100 + 60)
        for x in range(-64, 64):
            for z in range(-64, 64):
                self.world[(x, 0, z)] = ["bedrock", ["right", "left", "top", "bottom", "front", "back"]]
                for y in range(1, self.y_values[x + 64][z + 64] - 5):
                    self.world[(x, y, z)] = ["stone", ["right", "left", "top", "bottom", "front", "back"]]
                for y in range(self.y_values[x + 64][z + 64] - 5, self.y_values[x + 64][z + 64]):
                    self.world[(x, y, z)] = ["dirt", ["right", "left", "top", "bottom", "front", "back"]]
                self.world[(x, self.y_values[x + 64][z + 64], z)] = \
                    ["grass", ["right", "left", "top", "bottom", "front", "back"]]
        for pos in self.world:
            o_pos_dict = {"right": (pos[0] - 1, *pos[1:]),
                          "left": (pos[0] + 1, *pos[1:]),
                          "top": (pos[0], pos[1] - 1, pos[2]),
                          "bottom": (pos[0], pos[1] + 1, pos[2]),
                          "front": (*pos[0:2], pos[2] - 1),
                          "back": (*pos[0:2], pos[2] + 1)}
            for o_pos in o_pos_dict:
                if o_pos_dict[o_pos] in self.world:
                    self.world[o_pos_dict[o_pos]][1].remove(o_pos)
        instances = {"bedrock": {"right": numpy.array([], dtype=numpy.float32),
                                 "left": numpy.array([], dtype=numpy.float32),
                                 "top": numpy.array([], dtype=numpy.float32),
                                 "bottom": numpy.array([], dtype=numpy.float32),
                                 "front": numpy.array([], dtype=numpy.float32),
                                 "back": numpy.array([], dtype=numpy.float32)},
                     "stone": {"right": numpy.array([], dtype=numpy.float32),
                               "left": numpy.array([], dtype=numpy.float32),
                               "top": numpy.array([], dtype=numpy.float32),
                               "bottom": numpy.array([], dtype=numpy.float32),
                               "front": numpy.array([], dtype=numpy.float32),
                               "back": numpy.array([], dtype=numpy.float32)},
                     "dirt": {"right": numpy.array([], dtype=numpy.float32),
                              "left": numpy.array([], dtype=numpy.float32),
                              "top": numpy.array([], dtype=numpy.float32),
                              "bottom": numpy.array([], dtype=numpy.float32),
                              "front": numpy.array([], dtype=numpy.float32),
                              "back": numpy.array([], dtype=numpy.float32)},
                     "grass": {"right": numpy.array([], dtype=numpy.float32),
                               "left": numpy.array([], dtype=numpy.float32),
                               "top": numpy.array([], dtype=numpy.float32),
                               "bottom": numpy.array([], dtype=numpy.float32),
                               "front": numpy.array([], dtype=numpy.float32),
                               "back": numpy.array([], dtype=numpy.float32)}}
        for pos in self.world:
            for side in self.world[pos][1]:
                if len(instances[self.world[pos][0]][side]) > 0:
                    instances[self.world[pos][0]][side] = \
                        numpy.append(instances[self.world[pos][0]][side], numpy.array([pos], dtype=numpy.float32), 0)
                else:
                    instances[self.world[pos][0]][side] = numpy.array([pos], dtype=numpy.float32)
                # self.batch_3d.add(4, GL_QUADS, getattr(self.world[pos], f"{side}_tex"),
                #                   ("v3f", getattr(self.world[pos], f"{side}_pos")),
                #                   ("t2f", (0, 0, 1, 0, 1, 1, 0, 1)))
        for cube in instances:
            for side in instances[cube]:
                self.vaos_3d[cube].vaos[side].instance_update(instances[cube][side])
        self.camera.camera_pos[1] = self.y_values[64][64] + 1

    def mouse_callback(self, window, dx, dy):
        if not self.mouse_visibility:
            x_offset = dx - 1280 / 2
            y_offset = 720 / 2 - dy
            self.camera.process_mouse_movement(x_offset, y_offset)
            glfw.set_cursor_pos(self.window, 1280 / 2, 720 / 2)

    def key_callback(self, window, key, scancode, action, mode):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            if not self.mouse_visibility:
                glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)
                self.mouse_visibility = True
            else:
                glfw.set_window_should_close(self.window, True)
        if 0 <= key < 1024:
            if action == glfw.PRESS:
                self.keys[key] = True
            elif action == glfw.RELEASE:
                self.keys[key] = False

    def do_movement(self, time_s):
        net_movement = 4.317 * time_s
        if self.keys[glfw.KEY_W]:
            if self.sprint_delay > 0 and not self.holding_walk:
                self.sprinting = True
            elif self.sprint_delay == 0 and not self.holding_walk:
                self.sprint_delay = 0.25
            self.holding_walk = True
            if self.flying:
                if self.sprinting:
                    self.camera.process_keyboard("FRONT", net_movement * 5.0)
                else:
                    self.camera.process_keyboard("FRONT", net_movement * 2.5)
            elif self.crouching:
                self.camera.process_keyboard("FRONT", net_movement * 0.3)
            else:
                if self.sprinting:
                    self.camera.process_keyboard("FRONT", net_movement * 1.3)
                else:
                    self.camera.process_keyboard("FRONT", net_movement)
        else:
            self.holding_walk = False
            self.sprinting = False
        if self.keys[glfw.KEY_A]:
            if self.flying:
                self.camera.process_keyboard("SIDE", -net_movement * 2.5)
            elif self.crouching:
                self.camera.process_keyboard("SIDE", -net_movement * 0.3)
            else:
                self.camera.process_keyboard("SIDE", -net_movement)
        if self.keys[glfw.KEY_S]:
            if self.flying:
                self.camera.process_keyboard("FRONT", -net_movement * 2.5)
            elif self.crouching:
                self.camera.process_keyboard("FRONT", -net_movement * 0.3)
            else:
                self.camera.process_keyboard("FRONT", -net_movement)
        if self.keys[glfw.KEY_D]:
            if self.flying:
                self.camera.process_keyboard("SIDE", net_movement * 2.5)
            elif self.crouching:
                self.camera.process_keyboard("SIDE", net_movement * 0.3)
            else:
                self.camera.process_keyboard("SIDE", net_movement)
        x, y, z = self.camera.camera_pos
        x, y, z = self.check_value(x, 0.3), self.check_value(y, 0), self.check_value(z, 0.3)
        if self.keys[glfw.KEY_SPACE]:
            if self.fly_delay > 0 and not self.holding_jump:
                self.flying = not self.flying
                self.air_velocity = 0
                self.jumping = False
            elif self.fly_delay == 0 and not self.holding_jump:
                self.fly_delay = 0.25
            self.holding_jump = True
            if not self.jumping and not self.flying and \
                    ((int(x + 0.3), int(numpy.ceil(y - 1)), int(z + 0.3)) in self.world or
                     (int(x + 0.3), int(numpy.ceil(y - 1)), int(z - 0.3)) in self.world or
                     (int(x - 0.3), int(numpy.ceil(y - 1)), int(z + 0.3)) in self.world or
                     (int(x - 0.3), int(numpy.ceil(y - 1)), int(z - 0.3)) in self.world):
                self.air_velocity = 8.95142 * time_s
                self.camera.process_keyboard("UP", self.air_velocity)
                self.jumping = True
            if self.flying:
                self.camera.process_keyboard("UP", net_movement * 2)
        else:
            self.holding_jump = False
        if self.keys[glfw.KEY_LEFT_SHIFT]:
            if not self.crouching:
                self.camera.camera_pos[1] -= 0.125
                self.crouching = True
            if self.flying:
                self.camera.process_keyboard("UP", -net_movement * 2)
        elif self.crouching:
            self.camera.camera_pos[1] += 0.125
            self.crouching = False
        cx, cy, cz = self.camera.camera_pos
        if self.crouching:
            cy += 0.125
        cx, cy, cz = self.check_value(cx, 0.3), self.check_value(cy, 0), self.check_value(cz, 0.3)
        if (int(cx + 0.3), int(numpy.ceil(cy - 1)), int(cz + 0.3)) not in self.world and \
                (int(cx + 0.3), int(numpy.ceil(cy - 1)), int(cz - 0.3)) not in self.world and \
                (int(cx - 0.3), int(numpy.ceil(cy - 1)), int(cz + 0.3)) not in self.world and \
                (int(cx - 0.3), int(numpy.ceil(cy - 1)), int(cz - 0.3)) not in self.world and not self.flying:
            self.air_velocity -= 32 * time_s ** 2
            if (int(cx + 0.3), int(numpy.ceil(cy + self.air_velocity - 1)), int(cz + 0.3)) \
                    not in self.world and \
                    (int(cx + 0.3), int(numpy.ceil(cy + self.air_velocity - 1)), int(cz - 0.3)) \
                    not in self.world and \
                    (int(cx - 0.3), int(numpy.ceil(cy + self.air_velocity - 1)), int(cz + 0.3)) \
                    not in self.world and \
                    (int(cx - 0.3), int(numpy.ceil(cy + self.air_velocity - 1)), int(cz - 0.3)) \
                    not in self.world:
                if (int(cx + 0.3), int(numpy.ceil(cy + 1.85 + self.air_velocity - 1)), int(cz + 0.3)) \
                        not in self.world and \
                        (int(cx + 0.3), int(numpy.ceil(cy + 1.85 + self.air_velocity - 1)), int(cz - 0.3)) \
                        not in self.world and \
                        (int(cx - 0.3), int(numpy.ceil(cy + 1.85 + self.air_velocity - 1)), int(cz + 0.3)) \
                        not in self.world and \
                        (int(cx - 0.3), int(numpy.ceil(cy + 1.85 + self.air_velocity - 1)), int(cz - 0.3)) \
                        not in self.world:
                    self.camera.process_keyboard("UP", self.air_velocity)
                else:
                    if not self.crouching:
                        self.camera.camera_pos[1] = int(self.camera.camera_pos[1]) + 0.15
                    else:
                        self.camera.camera_pos[1] = int(self.camera.camera_pos[1]) + 0.025
                    self.air_velocity = 0
                    self.jumping = False
                    self.flying = False
            else:
                if not self.crouching:
                    self.camera.camera_pos[1] = round(self.camera.camera_pos[1])
                else:
                    self.camera.camera_pos[1] = round(self.camera.camera_pos[1]) - 0.125
                self.air_velocity = 0
                self.jumping = False
                self.flying = False
        elif not ((int(cx + 0.3), int(numpy.ceil(cy - 1)), int(cz + 0.3)) not in self.world and
                  (int(cx + 0.3), int(numpy.ceil(cy - 1)), int(cz - 0.3)) not in self.world and
                  (int(cx - 0.3), int(numpy.ceil(cy - 1)), int(cz + 0.3)) not in self.world and
                  (int(cx - 0.3), int(numpy.ceil(cy - 1)), int(cz - 0.3)) not in self.world):
            if not self.crouching:
                self.camera.camera_pos[1] = round(self.camera.camera_pos[1])
            else:
                self.camera.camera_pos[1] = round(self.camera.camera_pos[1]) - 0.125
            self.air_velocity = 0
            self.jumping = False
            self.flying = False
        elif not ((int(cx + 0.3), int(numpy.ceil(cy + 1.85 + self.air_velocity - 1)), int(cz + 0.3))
                  not in self.world and
                  (int(cx + 0.3), int(numpy.ceil(cy + 1.85 + self.air_velocity - 1)), int(cz - 0.3))
                  not in self.world and
                  (int(cx - 0.3), int(numpy.ceil(cy + 1.85 + self.air_velocity - 1)), int(cz + 0.3))
                  not in self.world and
                  (int(cx - 0.3), int(numpy.ceil(cy + 1.85 + self.air_velocity - 1)), int(cz - 0.3))
                  not in self.world):
            if not self.crouching:
                self.camera.camera_pos[1] = int(self.camera.camera_pos[1]) + 0.149
            else:
                self.camera.camera_pos[1] = int(self.camera.camera_pos[1]) + 0.024
        if self.sprint_delay > 0:
            self.sprint_delay -= time_s
        else:
            self.sprint_delay = 0
        if self.fly_delay > 0:
            self.fly_delay -= time_s
        else:
            self.fly_delay = 0
        if self.camera.camera_pos[1] < -64 and self.in_game:
            self.camera.camera_pos = pyrr.Vector3([0.0, self.y_values[64][64] + 1, 0.0])

    def mouse_button_check(self, time_s):
        mouse_buttons = glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_LEFT), \
                        glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_RIGHT)
        if self.breaking and (self.highlighted is None or self.breaking_block.tolist() != self.highlighted.tolist()):
            self.break_delay = 0.5
            self.breaking_block = self.highlighted
        if mouse_buttons[0]:
            if not self.mouse_visibility and self.highlighted is not None:
                if self.break_delay <= 0 and not self.breaking:
                    self.break_delay = 0.5
                    self.breaking = True
                    self.breaking_block = self.highlighted
                if self.break_delay <= 0 and self.breaking and self.world[tuple(self.highlighted)][0] != "bedrock":
                    px, py, pz = self.highlighted
                    px, py, pz = int(px), int(py), int(pz)
                    self.highlighted = tuple(self.highlighted)
                    for side in self.world[self.highlighted][1]:
                        self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_data = numpy.delete(
                            self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_data,
                            numpy.where((self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_data[:, 0] ==
                                         self.highlighted[0]) &
                                        (self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_data[:, 1] ==
                                         self.highlighted[1]) &
                                        (self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_data[:, 2] ==
                                         self.highlighted[2])), 0
                        )
                        self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_update()
                    del self.world[self.highlighted]
                    side_values = {"left": (px + 1, py, pz), "bottom": (px, py + 1, pz), "back": (px, py, pz + 1),
                                   "right": (px - 1, py, pz), "top": (px, py - 1, pz), "front": (px, py, pz - 1)}
                    for side in side_values:
                        x, y, z = side_values[side]
                        if (x, y, z) in self.world:
                            self.world[(x, y, z)][1].append(side)
                            if len(self.vaos_3d[self.world[(x, y, z)][0]].vaos[side].instance_data) > 0:
                                self.vaos_3d[self.world[(x, y, z)][0]].vaos[side].instance_data = numpy.append(
                                    self.vaos_3d[self.world[(x, y, z)][0]].vaos[side].instance_data,
                                    numpy.array([[x, y, z]], dtype=numpy.float32), 0
                                )
                            else:
                                self.vaos_3d[self.world[(x, y, z)][0]].vaos[side].instance_data = \
                                    numpy.array([[x, y, z]], dtype=numpy.float32)
                            self.vaos_3d[self.world[(x, y, z)][0]].vaos[side].instance_update()
                    self.highlighted = None
                    self.breaking_block = None
                    self.breaking = False
            else:
                self.break_delay = 0
                self.breaking = False
        else:
            self.break_delay = 0
            self.breaking = False
        if mouse_buttons[1]:
            if self.highlighted is not None and self.place_delay <= 0:
                new_block = self.block_face()
                x, y, z = self.camera.camera_pos
                if self.crouching:
                    y += 0.125
                x, y, z = self.check_value(x, 0.3), self.check_value(y, 0), self.check_value(z, 0.3)
                player_hitbox = ((int(x), int(y), int(z)),
                                 (int(x), int(y + 1), int(z)),
                                 (int(x), int(y + 1.85), int(z)),
                                 (int(x + 0.3), int(y), int(z + 0.3)),
                                 (int(x + 0.3), int(y), int(z - 0.3)),
                                 (int(x - 0.3), int(y), int(z + 0.3)),
                                 (int(x - 0.3), int(y), int(z - 0.3)),
                                 (int(x + 0.3), int(y + 1), int(z + 0.3)),
                                 (int(x + 0.3), int(y + 1), int(z - 0.3)),
                                 (int(x - 0.3), int(y + 1), int(z + 0.3)),
                                 (int(x - 0.3), int(y + 1), int(z - 0.3)),
                                 (int(x + 0.3), int(y + 1.85), int(z + 0.3)),
                                 (int(x + 0.3), int(y + 1.85), int(z - 0.3)),
                                 (int(x - 0.3), int(y + 1.85), int(z + 0.3)),
                                 (int(x - 0.3), int(y + 1.85), int(z - 0.3)))
                if new_block not in self.world and new_block not in player_hitbox and self.selected_block is not None:
                    self.place_delay = 0.25
                    visible_blocks = ["right", "left", "top", "bottom", "front", "back"]
                    bx, by, bz = new_block
                    side_values = {"left": (bx + 1, by, bz), "bottom": (bx, by + 1, bz), "back": (bx, by, bz + 1),
                                   "right": (bx - 1, by, bz), "top": (bx, by - 1, bz), "front": (bx, by, bz - 1)}
                    for side in side_values:
                        x, y, z = side_values[side]
                        if (x, y, z) in self.world:
                            if "ice" not in self.selected_block or "glass" not in self.selected_block:
                                self.vaos_3d[self.world[(x, y, z)][0]].vaos[side].instance_data = numpy.delete(
                                    self.vaos_3d[self.world[(x, y, z)][0]].vaos[side].instance_data,
                                    numpy.where(
                                        (self.vaos_3d[self.world[(x, y, z)][0]].vaos[side].instance_data[:, 0] == x) &
                                        (self.vaos_3d[self.world[(x, y, z)][0]].vaos[side].instance_data[:, 1] == y) &
                                        (self.vaos_3d[self.world[(x, y, z)][0]].vaos[side].instance_data[:, 2] == z)
                                    ), 0
                                )
                                self.vaos_3d[self.world[(x, y, z)][0]].vaos[side].instance_update()
                                if side == "right":
                                    visible_blocks.remove("left")
                                elif side == "left":
                                    visible_blocks.remove("right")
                                elif side == "top":
                                    visible_blocks.remove("bottom")
                                elif side == "bottom":
                                    visible_blocks.remove("top")
                                elif side == "front":
                                    visible_blocks.remove("back")
                                elif side == "back":
                                    visible_blocks.remove("front")
                    self.highlighted = tuple(self.highlighted)
                    side = ""
                    side_value = [int(new_block[axis] - self.highlighted[axis]) for axis in range(3)]
                    if side_value == [1, 0, 0]:
                        side = "right"
                    elif side_value == [-1, 0, 0]:
                        side = "left"
                    elif side_value == [0, 1, 0]:
                        side = "top"
                    elif side_value == [0, -1, 0]:
                        side = "bottom"
                    elif side_value == [0, 0, 1]:
                        side = "front"
                    elif side_value == [0, 0, -1]:
                        side = "back"
                    self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_data = numpy.delete(
                        self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_data,
                        numpy.where((self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_data[:, 0] ==
                                     self.highlighted[0]) &
                                    (self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_data[:, 1] ==
                                     self.highlighted[1]) &
                                    (self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_data[:, 2] ==
                                     self.highlighted[2])), 0
                    )
                    self.vaos_3d[self.world[self.highlighted][0]].vaos[side].instance_update()
                    self.highlighted = None
                    self.world[new_block] = [self.selected_block, visible_blocks]
                    for side in self.world[new_block][1]:
                        if len(self.vaos_3d[self.selected_block].vaos[side].instance_data) > 0:
                            self.vaos_3d[self.selected_block].vaos[side].instance_data = numpy.append(
                                self.vaos_3d[self.selected_block].vaos[side].instance_data,
                                numpy.array([new_block], dtype=numpy.float32), 0
                            )
                        else:
                            self.vaos_3d[self.selected_block].vaos[side].instance_data = \
                                numpy.array([new_block], dtype=numpy.float32)
                        self.vaos_3d[self.selected_block].vaos[side].instance_update()
        else:
            self.place_delay = 0
        if self.place_delay > 0:
            self.place_delay -= time_s
        if self.break_delay > 0:
            self.break_delay -= time_s

    def block_face(self):
        x, y, z = self.camera.camera_pos + self.ray_wor * (self.ray_i - 0.01)
        y += 1.62
        x, y, z = int(self.check_value(x, 0)), int(self.check_value(y, 0)), int(self.check_value(z, 0))
        hx, hy, hz = self.highlighted
        if (x, y, z) in ((hx + 1, hy, hz), (hx, hy + 1, hz), (hx, hy, hz + 1),
                         (hx - 1, hy, hz), (hx, hy - 1, hz), (hx, hy, hz - 1)):
            return x, y, z
        else:
            return hx, hy, hz

    def check_pos(self, axis, distance):
        x, y, z = self.camera.camera_pos
        if self.crouching:
            y += 0.125
        x, y, z = self.check_value(x, 0.3), self.check_value(y, 0), self.check_value(z, 0.3)
        crouch_counter = 0
        for i1, i2 in {(-.3, -.3), (-.3, .3), (.3, -.3), (.3, .3)}:
            ix, iy, iz = int(x + i1), y, int(z + i2)
            if (ix, int(iy), iz) in self.world or (ix, int(iy + 1), iz) in self.world or \
                    (ix, int(iy + 1.85), iz) in self.world:
                self.camera.camera_pos[axis] -= distance
                return
            elif self.crouching and not self.flying and not self.jumping \
                    and (ix, int(iy - 1), iz) not in self.world:
                crouch_counter += 1
        if crouch_counter >= 4:
            self.camera.camera_pos[axis] -= distance

    def window_resize(self, window, width, height):
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(90, width / height, 0.1, 100.0)
        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, projection)

    @staticmethod
    def check_value(value, limit):
        if value < limit:
            value -= 1
        return value


class Camera:
    def __init__(self, app):
        self.app = app
        self.camera_pos = pyrr.Vector3([0.0, 0.0, 0.0])
        self.camera_front = pyrr.Vector3([0.0, 0.0, -1.0])
        self.camera_up = pyrr.Vector3([0.0, 1.0, 0.0])
        self.camera_right = pyrr.Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.125
        self.yaw = -90.0
        self.pitch = 0.0

    def get_view_matrix(self):
        return self.look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def process_keyboard(self, direction, velocity):
        if direction == "FRONT":
            self.camera_pos[0] += numpy.cos(numpy.radians(self.yaw)) * velocity
            self.app.check_pos(0, numpy.cos(numpy.radians(self.yaw)) * velocity)
            self.camera_pos[2] += numpy.sin(numpy.radians(self.yaw)) * velocity
            self.app.check_pos(2, numpy.sin(numpy.radians(self.yaw)) * velocity)
        elif direction == "SIDE":
            self.camera_pos[0] += numpy.cos(numpy.radians(self.yaw) + numpy.pi / 2) * velocity
            self.app.check_pos(0, numpy.cos(numpy.radians(self.yaw) + numpy.pi / 2) * velocity)
            self.camera_pos[2] += numpy.sin(numpy.radians(self.yaw) + numpy.pi / 2) * velocity
            self.app.check_pos(2, numpy.sin(numpy.radians(self.yaw) + numpy.pi / 2) * velocity)
        elif direction == "UP":
            self.camera_pos[1] += velocity

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

        self.camera_front = pyrr.vector.normalise(front)
        self.camera_right = pyrr.vector.normalise(pyrr.vector3.cross(self.camera_front, pyrr.Vector3([0.0, 1.0, 0.0])))
        self.camera_up = pyrr.vector.normalise(pyrr.vector3.cross(self.camera_right, self.camera_front))

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


class VAO:
    def __init__(self, texture_file, vertex_data, index_data, instance_data=None):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertex_data.itemsize * 5, ctypes.c_void_p(0))
        self.ebo = glGenBuffers(1)
        self.indices = index_data
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertex_data.itemsize * 5, ctypes.c_void_p(12))
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        self.instance_vbo = glGenBuffers(1)
        self.instance_data = instance_data
        if self.instance_data is not None:
            self.instance_update(self.instance_data)

        self.texture = self.load_texture(texture_file)

        glBindVertexArray(0)

    def instance_update(self, instance_data=None):
        if instance_data is not None:
            self.instance_data = instance_data
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.instance_vbo)
        glBufferData(GL_ARRAY_BUFFER, self.instance_data.nbytes, self.instance_data.flatten(), GL_STATIC_DRAW)
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.instance_data.flatten().itemsize * 3, ctypes.c_void_p(0))
        glVertexAttribDivisor(2, 1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    @staticmethod
    def load_texture(texture_file):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        image = Image.open(texture_file)
        img_data = image.transpose(Image.FLIP_TOP_BOTTOM).tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glBindTexture(GL_TEXTURE_2D, 0)
        return texture


class Cube:
    front_v = numpy.array([
        0.0, 0.0, 1.0, 0.0, 0.0,
        1.0, 0.0, 1.0, 1.0, 0.0,
        1.0, 1.0, 1.0, 1.0, 1.0,
        0.0, 1.0, 1.0, 0.0, 1.0
    ], dtype=numpy.float32)
    back_v = numpy.array([
        1.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 1.0, 0.0,
        0.0, 1.0, 0.0, 1.0, 1.0,
        1.0, 1.0, 0.0, 0.0, 1.0
    ], dtype=numpy.float32)
    right_v = numpy.array([
        1.0, 0.0, 0.0, 1.0, 0.0,
        1.0, 1.0, 0.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 0.0, 1.0,
        1.0, 0.0, 1.0, 0.0, 0.0
    ], dtype=numpy.float32)
    left_v = numpy.array([
        0.0, 1.0, 0.0, 0.0, 1.0,
        0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 1.0, 0.0,
        0.0, 1.0, 1.0, 1.0, 1.0,
    ], dtype=numpy.float32)
    bottom_v = numpy.array([
        0.0, 0.0, 0.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 1.0, 0.0,
        1.0, 0.0, 1.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 0.0, 1.0,
    ], dtype=numpy.float32)
    top_v = numpy.array([
        1.0, 1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 1.0, 0.0,
        0.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 0.0, 1.0
    ], dtype=numpy.float32)
    indices = numpy.array([0, 1, 2, 2, 3, 0], dtype=numpy.uint32)

    def __init__(self, textures):  # textures: left, right, bottom, top, front, back
        left_vao = VAO(textures[0], Cube.left_v, Cube.indices)
        right_vao = VAO(textures[1], Cube.right_v, Cube.indices)
        bottom_vao = VAO(textures[2], Cube.bottom_v, Cube.indices)
        top_vao = VAO(textures[3], Cube.top_v, Cube.indices)
        front_vao = VAO(textures[4], Cube.front_v, Cube.indices)
        back_vao = VAO(textures[5], Cube.back_v, Cube.indices)
        self.vaos = {"left": left_vao, "right": right_vao, "bottom": bottom_vao,
                     "top": top_vao, "front": front_vao, "back": back_vao}


class TextManager:
    def __init__(self, app, character_size):
        self.app = app
        self.character_size = character_size
        character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 8.0 * character_size, 0.0, 0.0, 1.0,
                                 8.0 * character_size, 8.0 * character_size, 0.0, 1.0, 1.0,
                                 8.0 * character_size, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
        self.app.vaos_2d[f"character_{self.character_size}_ "] = VAO(
            character, QUAD_INDICES, QUAD_INDICES, (ASCII_PNG, (0, 16), (8, 8))
        )
        for char in CHARACTER_DICT:
            character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                                     0.0, 8.0 * character_size, 0.0, 0.0, 1.0,
                                     CHARACTER_DICT[char][0][1][0] * character_size,
                                     8.0 * character_size, 0.0, 1.0, 1.0,
                                     CHARACTER_DICT[char][0][1][0] * character_size, 0.0, 0.0, 1.0, 0.0],
                                    dtype=numpy.float32)
            self.app.vaos_2d[f"character_{self.character_size}_{char}"] = VAO(
                character, QUAD_INDICES, QUAD_INDICES, (ASCII_PNG, *CHARACTER_DICT[char][0])
            )
            character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                                     0.0, 8.0 * character_size, 0.0, 0.0, 1.0,
                                     CHARACTER_DICT[char][1][1][0] * character_size,
                                     8.0 * character_size, 0.0, 1.0, 1.0,
                                     CHARACTER_DICT[char][1][1][0] * character_size, 0.0, 0.0, 1.0, 0.0],
                                    dtype=numpy.float32)
            self.app.vaos_2d[f"character_{self.character_size}_{char.upper()}"] = VAO(
                character, QUAD_INDICES, QUAD_INDICES, (ASCII_PNG, *CHARACTER_DICT[char][1])
            )
        for char in SPECIAL_CHARACTER_DICT:
            character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                                     0.0, 8.0 * character_size, 0.0, 0.0, 1.0,
                                     SPECIAL_CHARACTER_DICT[char][1][0] * character_size,
                                     8.0 * character_size, 0.0, 1.0, 1.0,
                                     SPECIAL_CHARACTER_DICT[char][1][0] * character_size, 0.0, 0.0, 1.0, 0.0],
                                    dtype=numpy.float32)
            self.app.vaos_2d[f"character_{self.character_size}_{char}"] = VAO(
                character, QUAD_INDICES, QUAD_INDICES, (ASCII_PNG, *SPECIAL_CHARACTER_DICT[char])
            )

    def add_text(self, text, pos):
        for character in text:
            self.app.vaos_2d[f"character_{self.character_size}_{character}"].instances_update(
                self.app.vaos_2d[f"character_{self.character_size}_{character}"].instances.tolist() + [pos]
            )
            if character in CHARACTER_DICT:
                pos[0] += self.character_size * (CHARACTER_DICT[character][0][1][0] + 1)
            elif character.lower() in CHARACTER_DICT:
                pos[0] += self.character_size * (CHARACTER_DICT[character.lower()][1][1][0] + 1)
            elif character in SPECIAL_CHARACTER_DICT:
                pos[0] += self.character_size * (SPECIAL_CHARACTER_DICT[character][1][0] + 1)
            else:
                pos[0] += self.character_size * 5

    def remove_text(self, text, pos):
        for character in text:
            self.app.vaos_2d[f"character_{self.character_size}_{character}"].instances = numpy.delete(
                self.app.vaos_2d[f"character_{self.character_size}_{character}"].instances,
                numpy.where(
                    (self.app.vaos_2d[f"character_{self.character_size}_{character}"].instances[:, 0] == pos[0]) &
                    (self.app.vaos_2d[f"character_{self.character_size}_{character}"].instances[:, 1] == pos[1]) &
                    (self.app.vaos_2d[f"character_{self.character_size}_{character}"].instances[:, 2] == pos[2])
                ), 0
            )
            self.app.vaos_2d[f"character_{self.character_size}_{character}"].instances_update()
            if character in CHARACTER_DICT:
                pos[0] += self.character_size * (CHARACTER_DICT[character][0][1][0] + 1)
            elif character.lower() in CHARACTER_DICT:
                pos[0] += self.character_size * (CHARACTER_DICT[character.lower()][1][1][0] + 1)
            elif character in SPECIAL_CHARACTER_DICT:
                pos[0] += self.character_size * (SPECIAL_CHARACTER_DICT[character][1][0] + 1)
            else:
                pos[0] += self.character_size * 5

    def clear(self):
        for char in CHARACTER_DICT:
            if len(self.app.vaos_2d[f"character_{self.character_size}_{char}"].instances) > 0:
                self.app.vaos_2d[f"character_{self.character_size}_{char}"].instances_update([])
            if len(self.app.vaos_2d[f"character_{self.character_size}_{char.upper()}"].instances) > 0:
                self.app.vaos_2d[f"character_{self.character_size}_{char.upper()}"].instances_update([])
        for char in SPECIAL_CHARACTER_DICT:
            if len(self.app.vaos_2d[f"character_{self.character_size}_{char}"].instances) > 0:
                self.app.vaos_2d[f"character_{self.character_size}_{char}"].instances_update([])


if __name__ == '__main__':
    App(1280, 720, "False Worlds")
