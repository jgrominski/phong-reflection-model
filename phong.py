import math
import sys

import numpy as np
import pygame as pg
from pygame.locals import *

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
LIGHT_COLOR = (255, 255, 255)
SPHERE_RADIUS = 200
SCREEN_CENTER = (WIDTH // 2, HEIGHT // 2)
LIGHT_POSITION = (-600, -600, 1000)
AMBIENT_INTENSITY = 0.75
DIFFUSE_INTENSITY = 3.5
SPECULAR_INTENSITY = 1.5


def compute_normal(x, y, z):
    length = math.sqrt(x**2 + y**2 + z**2)
    return (x / length, y / length, z / length)


class PhongShading:

    def __init__(self, ambient_reflection, diffuse_reflection, specular_reflection, specular_exponent):
        self.ambient_reflection = ambient_reflection
        self.diffuse_reflection = diffuse_reflection
        self.specular_reflection = specular_reflection
        self.specular_exponent = specular_exponent

    def update_params(self, ambient_reflection, diffuse_reflection, specular_reflection, specular_exponent):
        self.ambient_reflection = ambient_reflection
        self.diffuse_reflection = diffuse_reflection
        self.specular_reflection = specular_reflection
        self.specular_exponent = specular_exponent

    def phong_shading(self, normal, view_direction, point):
        light_direction = np.array(LIGHT_POSITION) - point
        light_direction = light_direction / np.linalg.norm(light_direction)

        ambient = self.ambient_reflection * AMBIENT_INTENSITY

        diffuse = self.diffuse_reflection * \
            max(np.dot(normal, light_direction), 0) * DIFFUSE_INTENSITY

        reflection = 2 * np.dot(normal, light_direction) * \
            np.array(normal) - np.array(light_direction)
        specular = self.specular_reflection * \
            max(np.dot(reflection, view_direction),
                0) ** self.specular_exponent * SPECULAR_INTENSITY

        return ambient + diffuse + specular


class App:

    def __init__(self):
        self.colors = [
            (209, 121, 59),
            (26, 188, 156),
            (231, 76, 60),
            (234, 224, 200),
            (189, 195, 199)
        ]
        self.parameters = [
            (0.1236, 0.2965, 0.3126, 51.2),
            (0.15, 0.5, 0.7, 10),
            (0.1, 0.55, 0.7, 32),
            (0.11, 0.44, 0.1483, 11.264),
            (0.2313, 0.2775, 0.7739, 89.6)
        ]
        self.descriptions = [
            "Copper",
            "Turquoise Rubber",
            "Red Plastic",
            "Pearl",
            "Silver"
        ]
        self.material = 0

        self.phong = PhongShading(self.parameters[0][0], self.parameters[0][1],
                                  self.parameters[0][2], self.parameters[0][3])

        pg.init()
        pg.display.set_caption(
            "Phong Reflection Model: " + self.descriptions[0])
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.fps = 30

        self.main_loop()

    def render_sphere(self):
        self.phong.update_params(self.parameters[self.material][0], self.parameters[self.material][1],
                                 self.parameters[self.material][2], self.parameters[self.material][3])

        self.screen.fill(BACKGROUND_COLOR)

        for x in range(2 * SPHERE_RADIUS):
            for y in range(2 * SPHERE_RADIUS):
                x_coord = x - SPHERE_RADIUS
                y_coord = y - SPHERE_RADIUS
                z_squared = SPHERE_RADIUS ** 2 - x_coord ** 2 - y_coord ** 2

                if z_squared >= 0:
                    z_coord = math.sqrt(z_squared)
                    normal = compute_normal(x_coord, y_coord, z_coord)
                    view_direction = np.array((0, 0, 1))
                    point = np.array((x_coord, y_coord, z_coord))

                    shading = self.phong.phong_shading(
                        normal, view_direction, point)

                    sphere_color = self.colors[self.material]
                    color = (min(255, int(sphere_color[0] * shading)),
                             min(255, int(sphere_color[1] * shading)),
                             min(255, int(sphere_color[2] * shading)))

                    self.screen.set_at(
                        (x + SCREEN_CENTER[0] - SPHERE_RADIUS, y + SCREEN_CENTER[1] - SPHERE_RADIUS), color)

        pg.display.flip()
        pg.display.set_caption(
            "Phong Reflection Model: " + self.descriptions[self.material])

    def main_loop(self):
        self.render_sphere()

        running = True
        while running:
            for event in pg.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        if self.material != 0:
                            self.material = 0
                            self.render_sphere()
                    if event.key == K_2:
                        if self.material != 1:
                            self.material = 1
                            self.render_sphere()
                    if event.key == K_3:
                        if self.material != 2:
                            self.material = 2
                            self.render_sphere()
                    if event.key == K_4:
                        if self.material != 3:
                            self.material = 3
                            self.render_sphere()
                    if event.key == K_5:
                        if self.material != 4:
                            self.material = 4
                            self.render_sphere()

            self.clock.tick(self.fps)

        self.quit()

    def quit(self) -> None:
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    app = App()
