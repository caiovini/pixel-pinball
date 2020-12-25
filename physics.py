
import pygame as pg
import pymunk as pm

import math


class _Body():

    def __init__(self, position, mass, moment, body_type):
        self.body = pm.Body(mass=mass, moment=moment, body_type=body_type)
        self.body.position = position.x, position.y

    def rotate(self, image):
        
        # Rotate ball and keep its center

        try:
            orig_rect = image.get_rect()
            rot_image = pg.transform.rotate(
                image, -math.degrees(float(str(self.body.angle)[:5])))
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            return rot_image.subsurface(rot_rect).copy()
        except Exception as e:
            print(e)


class Circle(_Body):

    def __init__(self, position, collision_type, *, radius, body_type=pm.Body.DYNAMIC):

        mass = 1
        moment = pm.moment_for_circle(
            mass=mass, inner_radius=radius, outer_radius=radius)
        _Body.__init__(self, position, mass, moment, body_type)

        self.shape = pm.Circle(self.body, radius)
        self.shape.elasticity = 0.5
        self.shape.collision_type = collision_type

        if collision_type == 1:
            setattr(self.shape, "score", 0)


class Poly(_Body):

    def __init__(self, position, collision_type, *, radius, vertices, body_type=pm.Body.KINEMATIC):

        mass = 1
        moment = pm.moment_for_poly(mass=mass, vertices=vertices)
        _Body.__init__(self, position, mass, moment, body_type)
        self.shape = pm.Poly(self.body, vertices=vertices, radius=radius)

        self.shape.density = .01
        self.shape.elasticity = 4.5
        self.shape.friction = 0.5
        self.shape.collision_type = collision_type


def post_solve_lighthouse_ball(arbiter, space, _):
    shape, _ = arbiter.shapes
    shape.score += 1