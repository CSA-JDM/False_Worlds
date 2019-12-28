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


# region Constants
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
INDICES = numpy.array([0, 1, 2, 2, 3, 0], dtype=numpy.uint32)
HOTBAR = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 44.0, 0.0, 0.0, 1.0,
                      364.0, 44.0, 0.0, 1.0, 1.0,
                      364.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
ACTIVE_BAR = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 48.0, 0.0, 0.0, 1.0,
                          48.0, 48.0, 0.0, 1.0, 1.0,
                          48.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
HOTBAR_ICON = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                           0.0, 32.0, 0.0, 0.0, 1.0,
                           32.0, 32.0, 0.0, 1.0, 1.0,
                           32.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
CROSSHAIR_V = numpy.array([15.0, 0.0, 0.0, 0.0, 0.0,
                           15.0, 32.0, 0.0, 0.0, 1.0,
                           17.0, 32.0, 0.0, 1.0, 1.0,
                           17.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
CROSSHAIR_H = numpy.array([0.0, 15.0, 0.0, 0.0, 0.0,
                           0.0, 17.0, 0.0, 0.0, 1.0,
                           32.0, 17.0, 0.0, 1.0, 1.0,
                           32.0, 15.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
INVENTORY = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0, 332.0, 0.0, 0.0, 1.0,
                         352.0, 332.0, 0.0, 1.0, 1.0,
                         352.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
SCREEN = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 720.0, 0.0, 0.0, 1.0,
                      1280.0, 720.0, 0.0, 1.0, 1.0,
                      1280.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
BUTTON_OUTLINE = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                              0.0, 40.0, 0.0, 0.0, 1.0,
                              400.0, 40.0, 0.0, 1.0, 1.0,
                              400.0, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
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
ASCII_PNG = Image.open("textures/_ascii.png")
# endregion


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
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.make_context_current(self.window)
        # endregion

        # region Variables
        self.keys = [False] * 1024
        self.chunks = list()
        self.world = dict()
        self.mouse_visibility = True
        self.in_menu = True
        self.in_game = False
        self.in_inventory = False
        self.paused = False
        self.new_game = False
        self.selected_block = ""
        self.active_bar = 1
        self.highlighted = None
        self.breaking_block = None
        self.fps = 0
        self.width = 1280
        self.height = 720
        self.time_p = glfw.get_timer_value()
        shader = compileProgram(compileShader(open("vertex.glsl", "r").read(), GL_VERTEX_SHADER),
                                compileShader(open("fragment.glsl", "r").read(), GL_FRAGMENT_SHADER))
        self.projection_loc = glGetUniformLocation(shader, "projection")
        self.model_loc = glGetUniformLocation(shader, "model")
        self.view_loc = glGetUniformLocation(shader, "view")
        self.rotation_loc = glGetUniformLocation(shader, "rotation")
        self.player = Player(self)
        self.vaos_3d = dict()
        self.vaos_2d = dict()
        block_break = list()
        # endregion

        # region VAO Initialization
        self.char_2 = TextManager(self, 2)
        self.char_3 = TextManager(self, 3)
        self.char_4 = TextManager(self, 4)
        self.char_10 = TextManager(self, 10)
        self.vaos_3d["grass"] = Cube(["textures/grass.png"] * 2 + ["textures/dirt.png"] +
                                     ["textures/grass_top.png"] + ["textures/grass.png"] * 2)
        self.vaos_3d["grass_item"] = Item("grass", True, ["textures/grass.png"] * 2 + ["textures/dirt.png"] +
                                          ["textures/grass_top.png"] + ["textures/grass.png"] * 2)
        highlighted_vao = VAO("textures/_black.png", HIGHLIGHTED_CUBE, CUBE_INDICES_EDGES)
        block_list = list()
        for block in os.listdir("./textures"):
            if block[0] != "_" and "grass" not in block:
                self.vaos_3d[block.split(".")[0]] = Cube([f"textures/{block}"] * 6)
                self.vaos_3d[f"{block.split('.')[0]}_item"] = Item(block.split(".")[0], True, [f"textures/{block}"] * 6)
                block_list.append(f"textures/{block}")
        for stage in range(10):
            block_break.append(VAO.load_texture(f"textures/_destroy_stage_{stage}.png", transpose=True))
        self.vaos_2d["crosshair_v"] = VAO(
            "textures/_white.png", CROSSHAIR_V, INDICES, numpy.array([[624.0, 344.0, -0.6]], dtype=numpy.float32)
        )
        self.vaos_2d["crosshair_h"] = VAO(
            "textures/_white.png", CROSSHAIR_H, INDICES, numpy.array([[624.0, 344.0, -0.6]], dtype=numpy.float32)
        )
        self.vaos_2d["hotbar"] = VAO(
            "textures/_hotbar.png", HOTBAR, INDICES, numpy.array([[458.0, 676.0, -0.6]], dtype=numpy.float32)
        )
        self.vaos_2d["active_bar"] = VAO(
            "textures/_active_bar.png", ACTIVE_BAR, INDICES, numpy.array([[456.0, 674.0, -0.5]], dtype=numpy.float32)
        )
        for i in range(1, 10):
            self.vaos_2d[f"hotbar_{i}"] = VAO(
                "textures/_tp.png", HOTBAR_ICON, INDICES,
                numpy.array([[424.0 + i * 40, 682.0, -0.5]], dtype=numpy.float32)
            )
            self.vaos_2d[f"inventory_hotbar_slot_{i}"] = VAO(
                "textures/_tp.png", HOTBAR_ICON, INDICES,
                numpy.array([[444.0 + i * 36, 430.0, -0.3]], dtype=numpy.float32)
            )
        for i in range(1, 28):
            self.vaos_2d[f"inventory_slot_{i}"] = VAO(
                "textures/_tp.png", HOTBAR_ICON, INDICES,
                numpy.array([[480.0 + ((i - 1) % 9) * 36, 314.0 + int((i - 1) / 9) * 36, -0.3]], dtype=numpy.float32)
            )
        self.selected_block = self.vaos_2d["hotbar_1"].texture_name
        self.vaos_2d["inventory"] = VAO(
            "textures/_crafting_table.png", INVENTORY, INDICES, numpy.array([[464.0, 146.0, -0.3]], dtype=numpy.float32)
        )
        self.vaos_2d["active_inventory_slot"] = VAO(
            "textures/_white_tp.png", HOTBAR_ICON, INDICES
        )
        self.vaos_2d["paused"] = VAO(
            "textures/_black_tp.png", SCREEN, INDICES, numpy.array([[0.0, 0.0, -0.4]], dtype=numpy.float32)
        )
        self.vaos_2d["mouse_inventory"] = VAO(
            "textures/_tp.png", HOTBAR_ICON, INDICES
        )
        # endregion

        # region OpenGL Initialization
        glUseProgram(shader)
        glClearColor(135.0 / 255.0, 206.0 / 255.0, 235.0 / 255.0, 1.0)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLineWidth(4)  # todo figure out how large the outlines need to be for highlighted blocks
        self.projection_3d = pyrr.matrix44.create_perspective_projection_matrix(90, 1280 / 720, 0.1, 100.0)
        self.projection_2d = pyrr.matrix44.create_orthogonal_projection_matrix(0, 1280, 720, 0, 0.01, 100.0)
        translation_3d = pyrr.matrix44.create_from_translation([0.0, -1.65, 0.0])
        translation_2d = pyrr.matrix44.create_from_translation([0.0, 0.0, 0.0])
        view_2d = pyrr.matrix44.create_from_translation([0.0, 0.0, 0.0])
        rotation = pyrr.matrix33.create_from_matrix44(translation_2d)
        glUniformMatrix3fv(self.rotation_loc, 1, GL_FALSE, rotation)
        # endregion
        self.main_menu()

        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            old_fps = self.fps
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            time_n = glfw.get_timer_value()
            time_s = (time_n - self.time_p) / 10000000
            self.time_p = time_n
            self.mouse_button_check(time_s)
            view = self.player.get_view_matrix()

            if self.in_game:
                if self.new_game:
                    self.game_init()
                    # todo poll events?
                if not self.paused:
                    self.do_movement(time_s)
                    view = self.player.get_view_matrix()
                    mx, my = glfw.get_cursor_pos(self.window)
                    ray_nds = pyrr.Vector3([(2.0 * mx) / 1280 - 1.0, 1.0 - (2.0 * my) / 720, 1.0])
                    ray_clip = pyrr.Vector4([*ray_nds.xy, -1.0, 1.0])
                    ray_eye = pyrr.Vector4(numpy.dot(numpy.linalg.inv(self.projection_3d), ray_clip))
                    ray_eye = pyrr.Vector4([*ray_eye.xy, -1.0, 0.0])
                    ray_wor = (numpy.linalg.inv(view) * ray_eye).xyz
                    self.ray_wor = pyrr.vector.normalise(ray_wor)
                    self.s_ray_wor = self.player.player_pos.copy()
                    self.s_ray_wor[1] += 1.62
                    self.s_ray_wor = [int(self.check_value(axis, 0)) for axis in self.s_ray_wor]
                    self.e_ray_wor = self.player.player_pos + (self.ray_wor * 4)
                    self.e_ray_wor[1] += 1.62
                    self.e_ray_wor = [int(self.check_value(axis, 0)) for axis in self.e_ray_wor]
                    self.ray_i = 4
                    air = True
                    values = list()
                    for pos in range(3):
                        step = -1 if self.e_ray_wor[pos] < self.s_ray_wor[pos] else 1
                        for value in range(self.s_ray_wor[pos], self.e_ray_wor[pos] + step, step):
                            value -= self.player.player_pos[pos]
                            if pos == 1:
                                value -= 1.62
                            i = (value / self.ray_wor[pos])
                            if i not in values:  # todo clean up code below
                                values.append(i)
                                ray_cam = self.player.player_pos + (self.ray_wor * i)
                                ray_cam[1] += 1.62
                                orig_ray_cam = ray_cam.copy()
                                ray_cam[pos] -= 1
                                if ray_cam[pos] < 0:
                                    ray_cam[pos] += 0.5  # arbitrary number between 0 and 1 to fix rounding ex: -2 -> -3
                                try:
                                    ray_cam = numpy.array([int(self.check_value(axis, 0)) for axis in ray_cam])
                                except (OverflowError, ValueError):
                                    pass
                                if tuple(ray_cam) in self.world and 0 < values[-1] < self.ray_i:
                                    air = False
                                    self.highlighted = numpy.array(ray_cam, dtype=numpy.float32)
                                    self.ray_cam = ray_cam.copy()
                                    self.ray_i = values[-1]
                                # Copied portion below may not be necessary; a different fix probably exists
                                ray_cam = orig_ray_cam.copy()
                                if ray_cam[pos] < 0:
                                    ray_cam[pos] += 0.5  # arbitrary number between 0 and 1 to fix rounding ex: -2 -> -3
                                try:
                                    ray_cam = numpy.array([int(self.check_value(axis, 0)) for axis in ray_cam])
                                except (OverflowError, ValueError):
                                    pass
                                if tuple(ray_cam) in self.world and 0 < values[-1] < self.ray_i:
                                    air = False
                                    self.highlighted = numpy.array(ray_cam, dtype=numpy.float32)
                                    self.ray_cam = ray_cam.copy()
                                    self.ray_i = values[-1]
                    if self.highlighted is not None and air:
                        self.highlighted = None
                if self.in_inventory:
                    mx, my = glfw.get_cursor_pos(self.window)
                    self.vaos_2d["mouse_inventory"].instance_update(numpy.array(
                        [[mx * (1280 / self.width), my * (720 / self.height), -0.1]], dtype=numpy.float32
                    ))

            glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, self.projection_3d)
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, translation_3d)
            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view)
            item_list = list()
            for cube in self.vaos_3d.values():
                if isinstance(cube, Cube):
                    for vao in cube.vaos.values():
                        glBindVertexArray(vao.vao)
                        if vao.instance_data is not None:
                            glBindTexture(GL_TEXTURE_2D, vao.texture)
                            glDrawElementsInstanced(
                                GL_TRIANGLES, len(vao.indices), GL_UNSIGNED_INT, None, int(len(vao.instance_data))
                            )
                            glBindTexture(GL_TEXTURE_2D, 0)
                        glBindVertexArray(0)
                elif isinstance(cube, Item):
                    item_list.append(cube)
            for item in item_list:  # todo make item rotation more efficient
                if item.rotation_matrix is not None:
                    glUniformMatrix3fv(self.rotation_loc, 1, GL_FALSE, item.rotation_matrix)
                    for vao in item.vaos.values():
                        glBindVertexArray(vao.vao)
                        if vao.instance_data is not None:
                            glBindTexture(GL_TEXTURE_2D, vao.texture)
                            glDrawElementsInstanced(
                                GL_TRIANGLES, len(vao.indices), GL_UNSIGNED_INT, None, int(len(vao.instance_data))
                            )
                            glBindTexture(GL_TEXTURE_2D, 0)
                        glBindVertexArray(0)
            glUniformMatrix3fv(self.rotation_loc, 1, GL_FALSE, rotation)

            if self.highlighted is not None:
                if not numpy.array_equal(self.highlighted, highlighted_vao.instance_data):
                    highlighted_vao.instance_update(self.highlighted)
                glBindVertexArray(highlighted_vao.vao)
                if self.player.breaking:
                    if self.player.break_delay >= 0:
                        glBindTexture(GL_TEXTURE_2D, block_break[
                            int(-(self.player.break_delay - (0.5 - (0.5 / 10))) / (0.5 / 10))
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

            glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, self.projection_2d)
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, translation_2d)
            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view_2d)
            for vao in self.vaos_2d:
                if ("inventory" in vao and self.in_inventory) or (vao == "paused" and self.paused) or \
                        ("button" in vao and self.in_menu) or ("character_3" in vao and self.in_menu) or \
                        ("bar" in vao and self.in_game and "inventory" not in vao) or \
                        ("cross" in vao and self.in_game) or \
                        ("inventory" not in vao and vao != "paused" and "button" not in vao and
                         "character_3" not in vao and "bar" not in vao and "cross" not in vao):
                    glBindVertexArray(self.vaos_2d[vao].vao)
                    if self.vaos_2d[vao].instance_data is not None:
                        glBindTexture(GL_TEXTURE_2D, self.vaos_2d[vao].texture)
                        glDrawElementsInstanced(
                            GL_TRIANGLES, len(self.vaos_2d[vao].indices), GL_UNSIGNED_INT, None,
                            int(len(self.vaos_2d[vao].instance_data))
                        )
                        glBindTexture(GL_TEXTURE_2D, 0)
                    glBindVertexArray(0)

            self.fps = round(time_s ** -1)
            self.char_2.remove_text(f"{old_fps}", [1240.0, 20.0, -0.4])
            self.char_2.add_text(f"{self.fps}", [1240.0, 20.0, -0.4])
            glfw.swap_buffers(self.window)

        glfw.terminate()

    def main_menu(self):
        self.char_10.add_text("False Worlds", [315.0, 120.0, -0.4])
        self.vaos_2d["new_game_button_outline"] = VAO(
            "textures/_normal_button_outline.png", BUTTON_OUTLINE, INDICES,
            numpy.array([[440.0, 290.0, -0.3]], dtype=numpy.float32)
        )
        self.vaos_2d["quit_button_outline"] = VAO(
            "textures/_normal_button_outline.png", BUTTON_OUTLINE, INDICES,
            numpy.array([[440.0, 340.0, -0.3]], dtype=numpy.float32)
        )
        self.char_3.add_text("New Game", [565.0, 300.0, -0.3])
        self.char_3.add_text("Quit", [610.0, 350.0, -0.3])
        self.char_2.add_text(f"{self.fps}", [1240.0, 20.0, -0.4])

    def game_init(self):
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        self.mouse_visibility = False
        self.in_menu = False
        self.in_game = False
        self.player.jumping = False
        self.player.crouching = False
        self.highlighted = None
        self.player.air_vel = 0

        # region Instructions
        self.char_4.add_text("Controls:", [200.0, 280.0, -0.4])
        self.char_2.add_text("* W - Walk forwards", [220.0, 340.0 - 10.0, -0.4])
        self.char_2.add_text("* A - Walk backwards", [220.0, 360.0 - 10.0, -0.4])
        self.char_2.add_text("* S - Walk to the left", [220.0, 380.0 - 10.0, -0.4])
        self.char_2.add_text("* D - Walk to the right", [220.0, 400.0 - 10.0, -0.4])
        self.char_2.add_text("* Left Mouse Button - Break the highlighted block", [220.0, 420.0 - 10.0, -0.4])
        self.char_2.add_text("* Right Mouse Button - Place at side of highlighted block",
                             [220.0, 440.0 - 10.0, -0.4])
        self.char_2.add_text("* Space - Jump", [220.0, 460.0 - 10.0, -0.4])
        self.char_2.add_text("* Shift - Crouch", [220.0, 480.0 - 10.0, -0.4])
        self.char_2.add_text("* 1 to 9 - Switch which slot is active in the hotbar or action bar",
                             [220.0, 500.0 - 10.0, -0.4])
        self.char_2.add_text("* E - Access inventory", [220.0, 520.0 - 10.0, -0.4])
        self.char_2.add_text("* Esc - Pause game and open menu", [220.0, 540.0 - 10.0, -0.4])
        self.char_2.add_text("* P - Respawn at starting position", [220.0, 560.0 - 10.0, -0.4])
        self.char_4.add_text("Loading...", [548.0, 600.0, -0.4])
        for vao in self.vaos_2d:
            if ("inventory" in vao and self.in_inventory) or (vao == "paused" and self.paused) or \
                    ("button" in vao and self.in_menu) or ("character_3" in vao and self.in_menu) or \
                    ("bar" in vao and self.in_game and "inventory" not in vao) or \
                    ("cross" in vao and self.in_game) or \
                    ("inventory" not in vao and vao != "paused" and "button" not in vao and
                     "character_3" not in vao and "bar" not in vao and "cross" not in vao):
                glBindVertexArray(self.vaos_2d[vao].vao)
                if self.vaos_2d[vao].instance_data is not None:
                    glBindTexture(GL_TEXTURE_2D, self.vaos_2d[vao].texture)
                    glDrawElementsInstanced(
                        GL_TRIANGLES, len(self.vaos_2d[vao].indices), GL_UNSIGNED_INT, None,
                        int(len(self.vaos_2d[vao].instance_data))
                    )
                    glBindTexture(GL_TEXTURE_2D, 0)
                glBindVertexArray(0)
        glfw.swap_buffers(self.window)
        # endregion

        # region World Initialization
        self.chunks.clear()
        self.world.clear()
        size = [1024, 1024]
        scale = 100.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        base = random.randint(0, 1024)
        y_values = numpy.zeros(size, dtype=numpy.int32)
        for i in range(size[0]):
            for j in range(size[1]):
                y_values[i][j] = int(noise.pnoise2(
                    i / scale, j / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity,
                    repeatx=size[0], repeaty=size[1], base=base
                ) * 100 + 60)
        for cx, cz in [[x, z] for x in range(-1, 2) for z in range(-1, 2)]:
            for x in range(cx * 16, cx * 16 + 16):
                for z in range(cz * 16, cz * 16 + 16):
                    self.world[(x, 0, z)] = Block("bedrock")
                    for y in range(1, y_values[x + 512][z + 512] - 5):
                        self.world[(x, y, z)] = Block("stone")
                    for y in range(y_values[x + 512][z + 512] - 5, y_values[x + 512][z + 512]):
                        self.world[(x, y, z)] = Block("dirt")
                    self.world[(x, y_values[x + 512][z + 512], z)] = Block("grass")
        for pos in self.world:
            o_pos_dict = {"right": (pos[0] - 1, *pos[1:]),
                          "left": (pos[0] + 1, *pos[1:]),
                          "top": (pos[0], pos[1] - 1, pos[2]),
                          "bottom": (pos[0], pos[1] + 1, pos[2]),
                          "front": (*pos[0:2], pos[2] - 1),
                          "back": (*pos[0:2], pos[2] + 1)}
            for o_pos in o_pos_dict:
                if o_pos_dict[o_pos] in self.world:
                    self.world[o_pos_dict[o_pos]].faces.remove(o_pos)
        instance_data = {"bedrock": {"right": numpy.array([], dtype=numpy.float32),
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
            for side in self.world[pos].faces:
                if len(instance_data[self.world[pos].block_type][side]) > 0:
                    instance_data[self.world[pos].block_type][side] = \
                        numpy.append(
                            instance_data[self.world[pos].block_type][side], numpy.array([pos], dtype=numpy.float32), 0
                        )
                else:
                    instance_data[self.world[pos].block_type][side] = numpy.array([pos], dtype=numpy.float32)
        for cube in instance_data:
            for side in instance_data[cube]:
                self.vaos_3d[cube].vaos[side].instance_update(instance_data[cube][side])
        # endregion

        self.char_4.remove_text("Loading...", [548.0, 600.0, -0.4])
        self.char_4.add_text("Press any key to continue", [380.0, 600.0, -0.4])

    def mouse_callback(self, window, dx, dy):
        if not self.mouse_visibility:
            x_offset = dx - self.width / 2
            y_offset = self.height / 2 - dy
            self.player.process_mouse_movement(x_offset, y_offset)
            glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2)
        elif self.mouse_visibility:
            if self.in_menu:
                if "return_button_outline" in self.vaos_2d:
                    if (440 / 1280) * self.width < dx < ((440 + 400) / 1280) * self.width and \
                            (240 / 720) * self.height < dy < ((240 + 40) / 720) * self.height:
                        if self.vaos_2d["return_button_outline"].texture_name != \
                                "textures/_highlighted_button_outline.png":
                            self.vaos_2d["return_button_outline"].texture_name = \
                                "textures/_highlighted_button_outline.png"
                            self.vaos_2d["return_button_outline"].texture = \
                                VAO.load_texture("textures/_highlighted_button_outline.png")
                    elif self.vaos_2d["return_button_outline"].texture_name != "textures/_normal_button_outline.png":
                        self.vaos_2d["return_button_outline"].texture_name = "textures/_normal_button_outline.png"
                        self.vaos_2d["return_button_outline"].texture = \
                            VAO.load_texture("textures/_normal_button_outline.png")
                if (440 / 1280) * self.width < dx < ((440 + 400) / 1280) * self.width and \
                        (290 / 720) * self.height < dy < ((290 + 40) / 720) * self.height:
                    if self.vaos_2d["new_game_button_outline"].texture_name != "_highlighted_button_outline":
                        self.vaos_2d["new_game_button_outline"].texture_name = "_highlighted_button_outline"
                        self.vaos_2d["new_game_button_outline"].texture = \
                            VAO.load_texture("textures/_highlighted_button_outline.png")
                elif self.vaos_2d["new_game_button_outline"].texture_name != "_normal_button_outline":
                    self.vaos_2d["new_game_button_outline"].texture_name = "_normal_button_outline"
                    self.vaos_2d["new_game_button_outline"].texture = \
                        VAO.load_texture("textures/_normal_button_outline.png")
                if (440 / 1280) * self.width < dx < ((440 + 400) / 1280) * self.width and \
                        (340 / 720) * self.height < dy < ((340 + 40) / 720) * self.height:
                    if self.vaos_2d["quit_button_outline"].texture_name != "_highlighted_button_outline":
                        self.vaos_2d["quit_button_outline"].texture_name = "_highlighted_button_outline"
                        self.vaos_2d["quit_button_outline"].texture = \
                            VAO.load_texture("textures/_highlighted_button_outline.png")
                elif self.vaos_2d["quit_button_outline"].texture_name != "_normal_button_outline":
                    self.vaos_2d["quit_button_outline"].texture_name = "_normal_button_outline"
                    self.vaos_2d["quit_button_outline"].texture = \
                        VAO.load_texture("textures/_normal_button_outline.png")
            if self.in_inventory:
                for vao in self.vaos_2d:
                    if "slot" in vao and "inventory" in vao and "active" not in vao:
                        instance = tuple(self.vaos_2d[vao].instance_data[0])
                        if (int(instance[0]) / 1280) * self.width < dx < ((int(instance[0]) + 32) / 1280) * \
                                self.width and (int(instance[1]) / 720) * self.height < dy < \
                                ((int(instance[1]) + 32) / 720) * self.height:
                            self.vaos_2d["active_inventory_slot"].instance_update(numpy.array(
                                [[int(instance[0]), int(instance[1]), -0.2]], dtype=numpy.float32
                            ))
                            break
                        else:
                            self.vaos_2d["active_inventory_slot"].instance_update(numpy.array([], dtype=numpy.float32))

    def scroll_callback(self, window, dx, dy):
        if dy > 0:
            if not self.paused:
                new_hotbar = int((self.vaos_2d["active_bar"].instance_data[0][0] - 416.0) / 40.0 - 1.0)
                if new_hotbar < 1:
                    new_hotbar = 9
                self.selected_block = self.vaos_2d[f"hotbar_{new_hotbar}"].texture_name
                self.vaos_2d["active_bar"].instance_data = numpy.array(
                    [[new_hotbar * 40.0 + 416.0, 674.0, -0.5]], dtype=numpy.float32
                )
                self.vaos_2d["active_bar"].instance_update()
        elif dy < 0:
            if not self.paused:
                new_hotbar = int((self.vaos_2d["active_bar"].instance_data[0][0] - 416.0) / 40.0 + 1.0)
                if new_hotbar > 9:
                    new_hotbar = 1
                self.selected_block = self.vaos_2d[f"hotbar_{new_hotbar}"].texture_name
                self.vaos_2d["active_bar"].instance_data = numpy.array(
                    [[new_hotbar * 40.0 + 416.0, 674.0, -0.5]], dtype=numpy.float32
                )
                self.vaos_2d["active_bar"].instance_update()

    def mouse_button_callback(self, window, button, action, mods):
        mouse_pos = glfw.get_cursor_pos(window)
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            if self.mouse_visibility:
                if self.in_menu:
                    if (440 / 1280) * self.width < mouse_pos[0] < ((440 + 400) / 1280) * self.width and \
                            (240 / 720) * self.height < mouse_pos[1] < ((240 + 40) / 720) * self.height:
                        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
                        self.mouse_visibility = False
                        glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2)
                        self.paused = False
                        self.in_menu = False
                    elif (440 / 1280) * self.width < mouse_pos[0] < ((440 + 400) / 1280) * self.width and \
                            (290 / 720) * self.height < mouse_pos[1] < ((290 + 40) / 720) * self.height:
                        self.paused = False
                        self.in_game = True
                        self.new_game = True
                    elif (440 / 1280) * self.width < mouse_pos[0] < ((440 + 400) / 1280) * self.width and \
                            (340 / 720) * self.height < mouse_pos[1] < ((340 + 40) / 720) * self.height:
                        glfw.set_window_should_close(window, True)
                if self.in_inventory:
                    if not ((464 / 1280) * self.width < mouse_pos[0] < ((464 + 352) / 1280) * self.width and (146 / 720)
                            * self.height < mouse_pos[1] < ((146 + 332) / 720) * self.height):
                        glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2)
                        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
                        self.mouse_visibility = False
                        self.paused = False
                        self.in_inventory = False
                    elif len(self.vaos_2d["active_inventory_slot"].instance_data) > 0:
                        instance = tuple(self.vaos_2d["active_inventory_slot"].instance_data[0])
                        if f"inventory_slot_{int(((int(instance[0]) - 444) / 36) + (int(instance[1]) - 314) / 4)}" in \
                                self.vaos_2d:
                            mouse_vao = \
                                f"inventory_slot_{int(((int(instance[0]) - 444) / 36) + (int(instance[1]) - 314) / 4)}"
                        elif f"inventory_hotbar_slot_{int(((int(instance[0]) - 444) / 36))}" in self.vaos_2d:
                            mouse_vao = f"inventory_hotbar_slot_{int(((int(instance[0]) - 444) / 36))}"
                        else:
                            mouse_vao = None
                        if mouse_vao is not None:
                            self.vaos_2d["mouse_inventory"].instance_update(numpy.array(
                                [[int(instance[0]), int(instance[1]), -0.3]], dtype=numpy.float32
                            ))
                            self.vaos_2d["mouse_inventory"].texture_name, \
                                self.vaos_2d[mouse_vao].texture_name = self.vaos_2d[mouse_vao].texture_name, \
                                self.vaos_2d["mouse_inventory"].texture_name
                            self.vaos_2d["mouse_inventory"].texture, self.vaos_2d[mouse_vao].texture = \
                                self.vaos_2d[mouse_vao].texture, self.vaos_2d["mouse_inventory"].texture
                            if "hotbar" in mouse_vao:
                                self.vaos_2d[f"hotbar_{mouse_vao[-1]}"].texture_name = \
                                    self.vaos_2d[mouse_vao].texture_name
                                self.vaos_2d[f"hotbar_{mouse_vao[-1]}"].texture = \
                                    self.vaos_2d[mouse_vao].texture
                                self.selected_block = self.vaos_2d[
                                    f"hotbar_{int((self.vaos_2d['active_bar'].instance_data[0][0] - 416.0) / 40.0)}"
                                ].texture_name

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
        elif key == glfw.KEY_E and action == glfw.PRESS:
            self.in_inventory = not self.in_inventory
            self.paused = not self.paused
            self.mouse_visibility = not self.mouse_visibility
            if self.mouse_visibility is True:
                glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)
            elif self.mouse_visibility is False:
                glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
            glfw.set_cursor_pos(self.window, self.width / 2, self.height / 2)
        elif key == glfw.KEY_P and action == glfw.PRESS:
            self.player.player_pos = [0.0, 101, 0.0]
        if 0 <= key < 1024:
            if action == glfw.PRESS:
                self.keys[key] = True
            elif action == glfw.RELEASE:
                self.keys[key] = False
        for i in range(1, 10):
            if key == getattr(glfw, f"KEY_{i}"):
                self.selected_block = self.vaos_2d[f"hotbar_{i}"].texture_name
                self.vaos_2d["active_bar"].instance_data = numpy.array(
                    [[416.0 + 40.0 * i, 674.0, -0.5]], dtype=numpy.float32
                )
                self.vaos_2d["active_bar"].instance_update()
        if self.new_game:
            self.player.player_pos = [0.0, 101, 0.0]
            self.char_2.clear()
            self.char_4.clear()
            self.char_10.clear()
            self.char_2.add_text(f"{self.fps}", [1240.0, 20.0, -0.4])
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
            self.mouse_visibility = False
            self.in_game = True
            self.new_game = False

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
        x, y, z = self.player.player_pos
        x, y, z = self.check_value(x, 0.3), self.check_value(y, 0), self.check_value(z, 0.3)
        if self.keys[glfw.KEY_SPACE]:
            if self.player.fly_delay > 0 and not self.player.holding_jump:
                self.player.flying = not self.player.flying
                self.player.air_vel = 0
                self.player.jumping = False
            elif self.player.fly_delay == 0 and not self.player.holding_jump:
                self.player.fly_delay = 0.25
            self.player.holding_jump = True
            if not self.player.jumping and not self.player.flying and \
                    ((int(x + 0.3), int(numpy.ceil(y - 1)), int(z + 0.3)) in self.world or
                     (int(x + 0.3), int(numpy.ceil(y - 1)), int(z - 0.3)) in self.world or
                     (int(x - 0.3), int(numpy.ceil(y - 1)), int(z + 0.3)) in self.world or
                     (int(x - 0.3), int(numpy.ceil(y - 1)), int(z - 0.3)) in self.world):
                self.player.air_vel = 8.95142
                self.player.process_keyboard("UP", self.player.air_vel * time_s)
                self.player.jumping = True
            if self.player.flying:
                self.player.process_keyboard("UP", net_movement * 2)
        else:
            self.player.holding_jump = False
        if self.keys[glfw.KEY_LEFT_SHIFT]:
            if not self.player.crouching:
                self.player.player_pos[1] -= 0.3
                self.player.crouching = True
            if self.player.flying:
                self.player.process_keyboard("UP", -net_movement * 2)
        elif self.player.crouching:
            self.player.player_pos[1] += 0.3
            self.player.crouching = False
        cx, cy, cz = self.player.player_pos
        if self.player.crouching:
            cy += 0.3
        cx, cy, cz = self.check_value(cx, 0.3), self.check_value(cy, 0), self.check_value(cz, 0.3)
        for item in self.vaos_3d:
            if "item" in item:
                self.vaos_3d[item].get_rotation(time_s)
                add_item = False
                for vao in self.vaos_3d[item].vaos:
                    if self.vaos_3d[item].vaos[vao].instance_data is not None:
                        for instance in self.vaos_3d[item].vaos[vao].instance_data:
                            pos = instance.copy()
                            pos[0] -= 0.5
                            pos[2] -= 0.5
                            pos = tuple(int(value) for value in pos)
                            if (int(cx), int(cy), int(cz)) == pos:
                                add_item = True
                                self.vaos_3d[item].vaos[vao].instance_data = numpy.delete(
                                    self.vaos_3d[item].vaos[vao].instance_data, numpy.where(
                                        (self.vaos_3d[item].vaos[vao].instance_data[:, 0] == instance[0]) &
                                        (self.vaos_3d[item].vaos[vao].instance_data[:, 1] == instance[1]) &
                                        (self.vaos_3d[item].vaos[vao].instance_data[:, 2] == instance[2])
                                    ), 0
                                )
                        self.vaos_3d[item].vaos[vao].instance_update()
                if add_item:
                    self.inventory_add(self.vaos_3d[item].item_name)
        if (int(cx + 0.3), int(numpy.ceil(cy - 1)), int(cz + 0.3)) not in self.world and \
                (int(cx + 0.3), int(numpy.ceil(cy - 1)), int(cz - 0.3)) not in self.world and \
                (int(cx - 0.3), int(numpy.ceil(cy - 1)), int(cz + 0.3)) not in self.world and \
                (int(cx - 0.3), int(numpy.ceil(cy - 1)), int(cz - 0.3)) not in self.world and not self.player.flying:
            if self.player.air_vel > -78.4:
                self.player.air_vel -= (32 - .4) * time_s  # .4 is drag (a force, aka Newtons, so might not work)
            if self.player.air_vel <= -78.4:
                self.player.air_vel = -78.4
            if (int(cx + 0.3), int(numpy.ceil(cy + self.player.air_vel * time_s - 1)), int(cz + 0.3)) \
                    not in self.world and \
                    (int(cx + 0.3), int(numpy.ceil(cy + self.player.air_vel * time_s - 1)), int(cz - 0.3)) \
                    not in self.world and \
                    (int(cx - 0.3), int(numpy.ceil(cy + self.player.air_vel * time_s - 1)), int(cz + 0.3)) \
                    not in self.world and \
                    (int(cx - 0.3), int(numpy.ceil(cy + self.player.air_vel * time_s - 1)), int(cz - 0.3)) \
                    not in self.world:
                if (int(cx + 0.3), int(numpy.ceil(cy + 1.85 + self.player.air_vel * time_s - 1)), int(cz + 0.3)) \
                        not in self.world and \
                        (int(cx + 0.3), int(numpy.ceil(cy + 1.85 + self.player.air_vel * time_s - 1)), int(cz - 0.3)) \
                        not in self.world and \
                        (int(cx - 0.3), int(numpy.ceil(cy + 1.85 + self.player.air_vel * time_s - 1)), int(cz + 0.3)) \
                        not in self.world and \
                        (int(cx - 0.3), int(numpy.ceil(cy + 1.85 + self.player.air_vel * time_s - 1)), int(cz - 0.3)) \
                        not in self.world:
                    self.player.process_keyboard("UP", self.player.air_vel * time_s)
                else:
                    if not self.player.crouching:
                        self.player.player_pos[1] = int(self.player.player_pos[1]) + 0.15
                    else:
                        self.player.player_pos[1] = int(self.player.player_pos[1]) - 0.15
                    self.player.air_vel = 0
                    self.player.jumping = False
                    self.player.flying = False
            else:
                if not self.player.crouching:
                    self.player.player_pos[1] = round(self.player.player_pos[1])
                else:
                    self.player.player_pos[1] = round(self.player.player_pos[1]) - 0.3
                self.player.air_vel = 0
                self.player.jumping = False
                self.player.flying = False
        elif not ((int(cx + 0.3), int(numpy.ceil(cy - 1)), int(cz + 0.3)) not in self.world and
                  (int(cx + 0.3), int(numpy.ceil(cy - 1)), int(cz - 0.3)) not in self.world and
                  (int(cx - 0.3), int(numpy.ceil(cy - 1)), int(cz + 0.3)) not in self.world and
                  (int(cx - 0.3), int(numpy.ceil(cy - 1)), int(cz - 0.3)) not in self.world):
            if not self.player.crouching:
                self.player.player_pos[1] = round(self.player.player_pos[1])
            else:
                self.player.player_pos[1] = round(self.player.player_pos[1]) - 0.3
            self.player.air_vel = 0
            self.player.jumping = False
            self.player.flying = False
        elif not ((int(cx + 0.3), int(numpy.ceil(cy + 1.85 + self.player.air_vel - 1)), int(cz + 0.3))
                  not in self.world and
                  (int(cx + 0.3), int(numpy.ceil(cy + 1.85 + self.player.air_vel - 1)), int(cz - 0.3))
                  not in self.world and
                  (int(cx - 0.3), int(numpy.ceil(cy + 1.85 + self.player.air_vel - 1)), int(cz + 0.3))
                  not in self.world and
                  (int(cx - 0.3), int(numpy.ceil(cy + 1.85 + self.player.air_vel - 1)), int(cz - 0.3))
                  not in self.world):
            if not self.player.crouching:
                self.player.player_pos[1] = int(self.player.player_pos[1]) + 0.149
            else:
                self.player.player_pos[1] = int(self.player.player_pos[1]) - 0.151
        if self.player.sprint_delay > 0:
            self.player.sprint_delay -= time_s
        else:
            self.player.sprint_delay = 0
        if self.player.fly_delay > 0:
            self.player.fly_delay -= time_s
        else:
            self.player.fly_delay = 0
        if self.player.player_pos[1] < -64 and self.in_game:
            self.player.player_pos = [0.0, 101, 0.0]

    def mouse_button_check(self, time_s):
        mouse_buttons = glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_LEFT), \
                        glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_RIGHT)
        if self.player.breaking and \
                (self.highlighted is None or self.breaking_block.tolist() != self.highlighted.tolist()):
            self.player.break_delay = 0.5
            self.breaking_block = self.highlighted
        if mouse_buttons[0]:
            if not self.mouse_visibility and self.highlighted is not None:
                if self.player.break_delay <= 0 and not self.player.breaking:
                    self.player.break_delay = 0.5
                    self.player.breaking = True
                    self.breaking_block = self.highlighted
                if self.player.break_delay <= 0 and self.player.breaking and \
                        self.world[tuple(self.highlighted)].block_type != "bedrock":
                    pos = self.highlighted.copy()
                    pos[0] += 0.5
                    pos[2] += 0.5
                    block_name = self.world[tuple(self.highlighted)].block_type
                    for vao in self.vaos_3d[f"{block_name}_item"].vaos:
                        if self.vaos_3d[f"{block_name}_item"].vaos[vao].instance_data is not None:
                            self.vaos_3d[f"{block_name}_item"].vaos[vao].instance_data = numpy.append(
                                self.vaos_3d[f"{block_name}_item"].vaos[vao].instance_data,
                                numpy.array([pos], dtype=numpy.float32), 0
                            )
                        else:
                            self.vaos_3d[f"{block_name}_item"].vaos[vao].instance_data = numpy.array(
                                [pos], dtype=numpy.float32
                            )
                        self.vaos_3d[f"{block_name}_item"].vaos[vao].instance_update()
                    px, py, pz = self.highlighted
                    px, py, pz = int(px), int(py), int(pz)
                    self.highlighted = tuple(self.highlighted)
                    for side in self.world[self.highlighted].faces:
                        self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_data = numpy.delete(
                            self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_data,
                            numpy.where(
                                (self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_data[:, 0] ==
                                 self.highlighted[0]) &
                                (self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_data[:, 1] ==
                                 self.highlighted[1]) &
                                (self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_data[:, 2] ==
                                 self.highlighted[2])
                            ), 0
                        )
                        self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_update()
                    del self.world[self.highlighted]
                    side_values = {"left": (px + 1, py, pz), "bottom": (px, py + 1, pz), "back": (px, py, pz + 1),
                                   "right": (px - 1, py, pz), "top": (px, py - 1, pz), "front": (px, py, pz - 1)}
                    for side in side_values:
                        x, y, z = side_values[side]
                        if (x, y, z) in self.world:
                            self.world[(x, y, z)].faces.append(side)
                            if self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side] is not None and \
                                    len(self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side].instance_data) > 0:
                                self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side].instance_data = numpy.append(
                                    self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side].instance_data,
                                    numpy.array([[x, y, z]], dtype=numpy.float32), 0
                                )
                            else:
                                self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side].instance_data = \
                                    numpy.array([[x, y, z]], dtype=numpy.float32)
                            self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side].instance_update()
                    self.highlighted = None
                    self.breaking_block = None
                    self.player.breaking = False
            else:
                self.player.break_delay = 0
                self.player.breaking = False
        else:
            self.player.break_delay = 0
            self.player.breaking = False
        if mouse_buttons[1]:
            if self.highlighted is not None and self.player.place_delay <= 0:
                new_block = self.block_face()
                x, y, z = self.player.player_pos
                if self.player.crouching:
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
                    self.player.place_delay = 0.25
                    visible_blocks = ["right", "left", "top", "bottom", "front", "back"]
                    bx, by, bz = new_block
                    side_values = {"left": (bx + 1, by, bz), "bottom": (bx, by + 1, bz), "back": (bx, by, bz + 1),
                                   "right": (bx - 1, by, bz), "top": (bx, by - 1, bz), "front": (bx, by, bz - 1)}
                    for side in side_values:
                        x, y, z = side_values[side]
                        if (x, y, z) in self.world:
                            if "ice" not in self.selected_block and "glass" not in self.selected_block:
                                self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side].instance_data = numpy.delete(
                                    self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side].instance_data,
                                    numpy.where(
                                        (self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side].instance_data[:, 0]
                                         == x) &
                                        (self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side].instance_data[:, 1]
                                         == y) &
                                        (self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side].instance_data[:, 2]
                                         == z)
                                    ), 0
                                )
                                self.vaos_3d[self.world[(x, y, z)].block_type].vaos[side].instance_update()
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
                    if "ice" not in self.selected_block and "glass" not in self.selected_block:
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
                        self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_data = numpy.delete(
                            self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_data,
                            numpy.where(
                                (self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_data[:, 0] ==
                                 self.highlighted[0]) &
                                (self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_data[:, 1] ==
                                 self.highlighted[1]) &
                                (self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_data[:, 2] ==
                                 self.highlighted[2])
                            ), 0
                        )
                        self.vaos_3d[self.world[self.highlighted].block_type].vaos[side].instance_update()
                    self.highlighted = None
                    self.world[new_block] = Block(self.selected_block)
                    self.world[new_block].faces = visible_blocks
                    for side in self.world[new_block].faces:
                        if self.vaos_3d[self.selected_block].vaos[side].instance_data is not None and \
                                len(self.vaos_3d[self.selected_block].vaos[side].instance_data) > 0:
                            self.vaos_3d[self.selected_block].vaos[side].instance_data = numpy.append(
                                self.vaos_3d[self.selected_block].vaos[side].instance_data,
                                numpy.array([new_block], dtype=numpy.float32), 0
                            )
                        else:
                            self.vaos_3d[self.selected_block].vaos[side].instance_data = \
                                numpy.array([new_block], dtype=numpy.float32)
                        self.vaos_3d[self.selected_block].vaos[side].instance_update()
        else:
            self.player.place_delay = 0
        if self.player.place_delay > 0:
            self.player.place_delay -= time_s
        if self.player.break_delay > 0:
            self.player.break_delay -= time_s

    def block_face(self):
        x, y, z = self.player.player_pos + self.ray_wor * (self.ray_i - 0.01)
        y += 1.62
        x, y, z = int(self.check_value(x, 0)), int(self.check_value(y, 0)), int(self.check_value(z, 0))
        hx, hy, hz = self.highlighted
        if (x, y, z) in ((hx + 1, hy, hz), (hx, hy + 1, hz), (hx, hy, hz + 1),
                         (hx - 1, hy, hz), (hx, hy - 1, hz), (hx, hy, hz - 1)):
            return x, y, z
        else:
            return hx, hy, hz

    def inventory_add(self, item):
        for i in range(1, 10):
            if self.player.hotbar[i - 1] is None:
                self.player.hotbar[i - 1] = item
                self.vaos_2d[f"hotbar_{i}"].texture_name = item
                self.vaos_2d[f"hotbar_{i}"].texture = VAO.load_texture(f"textures/{item}.png")
                self.vaos_2d[f"inventory_hotbar_slot_{i}"].texture_name = item
                self.vaos_2d[f"inventory_hotbar_slot_{i}"].texture = VAO.load_texture(f"textures/{item}.png")
                if i == self.active_bar:
                    self.selected_block = self.vaos_2d[f"hotbar_{i}"].texture_name
                return
        for i in range(1, 28):
            if self.player.inventory[i - 1] is None:
                self.player.inventory[i - 1] = item
                self.vaos_2d[f"inventory_slot_{i}"].texture_name = item
                self.vaos_2d[f"inventory_slot_{i}"].texture = VAO.load_texture(f"textures/{item}.png")
                return

    def check_pos(self, axis, distance):
        x, y, z = self.player.player_pos
        if self.player.crouching:
            y += 0.3
        x, y, z = self.check_value(x, 0.3), self.check_value(y, 0), self.check_value(z, 0.3)
        crouch_counter = 0
        for i1, i2 in {(-.3, -.3), (-.3, .3), (.3, -.3), (.3, .3)}:
            ix, iy, iz = int(x + i1), y, int(z + i2)
            if (ix, int(iy), iz) in self.world or (ix, int(iy + 1), iz) in self.world or \
                    (ix, int(iy + 1.85), iz) in self.world:
                self.player.player_pos[axis] -= distance
                return
            elif self.player.crouching and not self.player.flying and not self.player.jumping \
                    and (ix, int(iy - 1), iz) not in self.world:
                crouch_counter += 1
        if crouch_counter >= 4:
            self.player.player_pos[axis] -= distance

    def window_resize(self, window, width, height):
        glViewport(0, 0, width, height)
        self.projection_3d = pyrr.matrix44.create_perspective_projection_matrix(90, width / height, 0.1, 100.0)
        self.projection_2d = pyrr.matrix44.create_orthogonal_projection_matrix(0, width, height, 0, 0.01, 100.0)
        self.width, self.height = width, height

    @staticmethod
    def check_value(value, limit):
        if value < limit:
            value -= 1
        return value


class Camera:
    def __init__(self, app):
        self.app = app
        self.player_pos = [0.0, 0.0, 0.0]
        self.player_front = pyrr.Vector3([0.0, 0.0, -1.0])
        self.player_up = pyrr.Vector3([0.0, 1.0, 0.0])
        self.player_right = pyrr.Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.125
        self.yaw = -90.0
        self.pitch = 0.0

    def get_view_matrix(self):
        return self.look_at(self.player_pos, self.player_pos + self.player_front, self.player_up)

    def process_keyboard(self, direction, velocity):
        if direction == "FRONT":
            self.player_pos[0] += numpy.cos(numpy.radians(self.yaw)) * velocity
            self.app.check_pos(0, numpy.cos(numpy.radians(self.yaw)) * velocity)
            self.player_pos[2] += numpy.sin(numpy.radians(self.yaw)) * velocity
            self.app.check_pos(2, numpy.sin(numpy.radians(self.yaw)) * velocity)
        elif direction == "SIDE":
            self.player_pos[0] += numpy.cos(numpy.radians(self.yaw) + numpy.pi / 2) * velocity
            self.app.check_pos(0, numpy.cos(numpy.radians(self.yaw) + numpy.pi / 2) * velocity)
            self.player_pos[2] += numpy.sin(numpy.radians(self.yaw) + numpy.pi / 2) * velocity
            self.app.check_pos(2, numpy.sin(numpy.radians(self.yaw) + numpy.pi / 2) * velocity)
        elif direction == "UP":
            self.player_pos[1] += velocity

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

        self.player_front = pyrr.vector.normalise(front)
        self.player_right = pyrr.vector.normalise(pyrr.vector3.cross(self.player_front, pyrr.Vector3([0.0, 1.0, 0.0])))
        self.player_up = pyrr.vector.normalise(pyrr.vector3.cross(self.player_right, self.player_front))

    @staticmethod
    def look_at(position, target, world_up):
        z_axis = pyrr.vector.normalise(position - target)
        x_axis = pyrr.vector.normalise(pyrr.vector3.cross(pyrr.vector.normalise(world_up), z_axis))
        y_axis = pyrr.vector3.cross(z_axis, x_axis)

        translation = pyrr.Matrix44.identity()
        translation[3][0] = -position[0]
        translation[3][1] = -position[1]
        translation[3][2] = -position[2]

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


class Player(Camera):
    def __init__(self, app):
        super().__init__(app)
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


class VAO:
    def __init__(self, texture_file, vertex_data, index_data, instance_data=None, transpose=False):
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

        if isinstance(texture_file, str):
            self.texture_name = texture_file.split("/")[-1].split(".")[0]
        self.texture = self.load_texture(texture_file, transpose)

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
    def load_texture(texture_file, transpose=False):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        if isinstance(texture_file, str):
            # load image
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

    def __init__(self, textures):  # textures: left, right, bottom, top, front, back
        self.textures = textures
        left_vao = VAO(textures[0], Cube.left_v, INDICES, transpose=True)
        right_vao = VAO(textures[1], Cube.right_v, INDICES, transpose=True)
        bottom_vao = VAO(textures[2], Cube.bottom_v, INDICES, transpose=True)
        top_vao = VAO(textures[3], Cube.top_v, INDICES, transpose=True)
        front_vao = VAO(textures[4], Cube.front_v, INDICES, transpose=True)
        back_vao = VAO(textures[5], Cube.back_v, INDICES, transpose=True)
        self.vaos = {"left": left_vao, "right": right_vao, "bottom": bottom_vao,
                     "top": top_vao, "front": front_vao, "back": back_vao}


class Chunk:  # todo finish
    def __init__(self, pos):
        self.pos = pos
        self.data = numpy.zeros((16, 16, 16), dtype=numpy.int32)


class Block:  # todo finish
    def __init__(self, block_type):
        self.block_type = block_type
        self.faces = ["right", "left", "top", "bottom", "front", "back"]


class Item:
    front_v = numpy.array([
        -0.25, 0.0, 0.25, 0.0, 0.0,
        0.25, 0.0, 0.25, 1.0, 0.0,
        0.25, 0.5, 0.25, 1.0, 1.0,
        -0.25, 0.5, 0.25, 0.0, 1.0
    ], dtype=numpy.float32)
    back_v = numpy.array([
        0.25, 0.0, -0.25, 0.0, 0.0,
        -0.25, 0.0, -0.25, 1.0, 0.0,
        -0.25, 0.5, -0.25, 1.0, 1.0,
        0.25, 0.5, -0.25, 0.0, 1.0
    ], dtype=numpy.float32)
    right_v = numpy.array([
        0.25, 0.0, -0.25, 1.0, 0.0,
        0.25, 0.5, -0.25, 1.0, 1.0,
        0.25, 0.5, 0.25, 0.0, 1.0,
        0.25, 0.0, 0.25, 0.0, 0.0
    ], dtype=numpy.float32)
    left_v = numpy.array([
        -0.25, 0.5, -0.25, 0.0, 1.0,
        -0.25, 0.0, -0.25, 0.0, 0.0,
        -0.25, 0.0, 0.25, 1.0, 0.0,
        -0.25, 0.5, 0.25, 1.0, 1.0,
    ], dtype=numpy.float32)
    bottom_v = numpy.array([
        -0.25, 0.0, -0.25, 0.0, 0.0,
        0.25, 0.0, -0.25, 1.0, 0.0,
        0.25, 0.0, 0.25, 1.0, 1.0,
        -0.25, 0.0, 0.25, 0.0, 1.0,
    ], dtype=numpy.float32)
    top_v = numpy.array([
        0.25, 0.5, -0.25, 0.0, 0.0,
        -0.25, 0.5, -0.25, 1.0, 0.0,
        -0.25, 0.5, 0.25, 1.0, 1.0,
        0.25, 0.5, 0.25, 0.0, 1.0
    ], dtype=numpy.float32)

    def __init__(self, item_name, can_place, textures, pos=None):
        self.item_name = item_name
        self.can_place = can_place
        self.rotation_i = float()
        self.rotation_matrix = None
        self.vaos = {"front": VAO(textures[4], Item.front_v, INDICES, transpose=True),
                     "back": VAO(textures[5], Item.back_v, INDICES, transpose=True),
                     "left": VAO(textures[0], Item.left_v, INDICES, transpose=True),
                     "right": VAO(textures[1], Item.right_v, INDICES, transpose=True),
                     "top": VAO(textures[3], Item.top_v, INDICES, transpose=True),
                     "bottom": VAO(textures[2], Item.bottom_v, INDICES, transpose=True)}

    def get_rotation(self, time_s):  # todo add separate rotation matrices (aka make it an input for the vertex shader)
        self.rotation_i += time_s
        self.rotation_matrix = pyrr.matrix33.create_from_y_rotation(self.rotation_i)


class TextManager:
    def __init__(self, app, character_size):
        self.app = app
        self.character_size = character_size
        character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                                 0.0, 8.0 * character_size, 0.0, 0.0, 1.0,
                                 5.0 * character_size, 8.0 * character_size, 0.0, 1.0, 1.0,
                                 5.0 * character_size, 0.0, 0.0, 1.0, 0.0], dtype=numpy.float32)
        self.app.vaos_2d[f"character_{self.character_size}_ "] = VAO(
            (ASCII_PNG, (0, 16), (8, 8)), character, INDICES
        )
        for char in CHARACTER_DICT:
            character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                                     0.0, 8.0 * character_size, 0.0, 0.0, 1.0,
                                     CHARACTER_DICT[char][0][1][0] * character_size,
                                     8.0 * character_size, 0.0, 1.0, 1.0,
                                     CHARACTER_DICT[char][0][1][0] * character_size, 0.0, 0.0, 1.0, 0.0],
                                    dtype=numpy.float32)
            self.app.vaos_2d[f"character_{self.character_size}_{char}"] = VAO(
                (ASCII_PNG, *CHARACTER_DICT[char][0]), character, INDICES
            )
            character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                                     0.0, 8.0 * character_size, 0.0, 0.0, 1.0,
                                     CHARACTER_DICT[char][1][1][0] * character_size,
                                     8.0 * character_size, 0.0, 1.0, 1.0,
                                     CHARACTER_DICT[char][1][1][0] * character_size, 0.0, 0.0, 1.0, 0.0],
                                    dtype=numpy.float32)
            self.app.vaos_2d[f"character_{self.character_size}_{char.upper()}"] = VAO(
                (ASCII_PNG, *CHARACTER_DICT[char][1]), character, INDICES
            )
        for char in SPECIAL_CHARACTER_DICT:
            character = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0,
                                     0.0, 8.0 * character_size, 0.0, 0.0, 1.0,
                                     SPECIAL_CHARACTER_DICT[char][1][0] * character_size,
                                     8.0 * character_size, 0.0, 1.0, 1.0,
                                     SPECIAL_CHARACTER_DICT[char][1][0] * character_size, 0.0, 0.0, 1.0, 0.0],
                                    dtype=numpy.float32)
            self.app.vaos_2d[f"character_{self.character_size}_{char}"] = VAO(
                (ASCII_PNG, *SPECIAL_CHARACTER_DICT[char]), character, INDICES
            )

    def add_text(self, text, pos):
        for character in text:
            if self.app.vaos_2d[f"character_{self.character_size}_{character}"].instance_data is not None:
                self.app.vaos_2d[f"character_{self.character_size}_{character}"].instance_update(
                    numpy.array(
                        self.app.vaos_2d[f"character_{self.character_size}_{character}"].instance_data.tolist() + [pos],
                        dtype=numpy.float32
                    )
                )
            else:
                self.app.vaos_2d[f"character_{self.character_size}_{character}"].instance_update(
                    numpy.array([pos], dtype=numpy.float32)
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
            self.app.vaos_2d[f"character_{self.character_size}_{character}"].instance_data = numpy.delete(
                self.app.vaos_2d[f"character_{self.character_size}_{character}"].instance_data,
                numpy.where(
                    (self.app.vaos_2d[f"character_{self.character_size}_{character}"].instance_data[:, 0] == pos[0]) &
                    (self.app.vaos_2d[f"character_{self.character_size}_{character}"].instance_data[:, 1] == pos[1]) &
                    (self.app.vaos_2d[f"character_{self.character_size}_{character}"].instance_data[:, 2] == pos[2])
                ), 0
            )
            self.app.vaos_2d[f"character_{self.character_size}_{character}"].instance_update()
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
            if self.app.vaos_2d[f"character_{self.character_size}_{char}"].instance_data is not None and \
                    len(self.app.vaos_2d[f"character_{self.character_size}_{char}"].instance_data) > 0:
                self.app.vaos_2d[f"character_{self.character_size}_{char}"].instance_update(
                    numpy.array([], dtype=numpy.float32)
                )
            if self.app.vaos_2d[f"character_{self.character_size}_{char.upper()}"].instance_data is not None and \
                    len(self.app.vaos_2d[f"character_{self.character_size}_{char.upper()}"].instance_data) > 0:
                self.app.vaos_2d[f"character_{self.character_size}_{char.upper()}"].instance_update(
                    numpy.array([], dtype=numpy.float32)
                )
        for char in SPECIAL_CHARACTER_DICT:
            if self.app.vaos_2d[f"character_{self.character_size}_{char}"].instance_data is not None and \
                    len(self.app.vaos_2d[f"character_{self.character_size}_{char}"].instance_data) > 0:
                self.app.vaos_2d[f"character_{self.character_size}_{char}"].instance_update(
                    numpy.array([], dtype=numpy.float32)
                )


if __name__ == '__main__':
    App(1280, 720, "False Worlds")
