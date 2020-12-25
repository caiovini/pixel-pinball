import pygame as pg
import pymunk as pm

import sys
import math

from assets import SandTop, SandBottom, BorderTop, BorderBottom, PinballBar, PinballSmallBar, Buttons, Lighthouses, Ball
from physics import Circle, Poly, post_solve_lighthouse_ball
from os.path import join
from json import loads

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 1000

BLACK = pg.Color(0, 0, 0)
YELLOW = pg.Color(255, 255, 0)
WHITE = pg.Color(255, 255, 255)
RED = pg.Color(255, 0, 0)

space_step = 1/60
clock = pg.time.Clock()

collisions_file = join("assets", "collisions.json")

def main() -> None:
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Pixel pinball")

    space = pm.Space()
    space.gravity = (0.0, 800.0)

    font = pg.font.Font(join("fonts", "segoe-ui-symbol.ttf"), 20)
    alpha_bg = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    alpha_bg.set_alpha(228)
    alpha_bg.fill((BLACK))


    sand_top = SandTop()
    sand_bottom = SandBottom()
    border_top = BorderTop()
    border_bottom = BorderBottom()
    pinball_bar = PinballBar()
    pinball_small_bar = PinballSmallBar()
    buttons = Buttons()
    lighthouses = Lighthouses()
    ball = Ball()

    sand_bottom.set_position(0, SCREEN_HEIGHT - sand_bottom.rect.h)
    border_bottom.set_position(0, SCREEN_HEIGHT - border_bottom.rect.h)
    pinball_bar.set_position(10, sand_bottom.rect.y - sand_bottom.rect.h)
    pinball_small_bar.set_position(
        pinball_bar.rect.x + 40, pinball_bar.rect.y + 70)
    buttons.set_position(175, pinball_small_bar.rect.y + 50)
    lighthouses.set_position(200, sand_top.rect.y + 200)

    # Initial position for the ball
    ball.set_position(570, 300)
    ball_ = Circle(ball.rect, 1, radius=10)

    left_button_vertices = [pm.Vec2d(0, 0), pm.Vec2d(35, 90), pm.Vec2d(-5, 60)]
    left_button = Poly(pg.Rect((185, 520), (0, 0)), 2, radius=0.5, vertices=left_button_vertices)

    right_button_vertices = [pm.Vec2d(0, 0), pm.Vec2d(-35, 80), pm.Vec2d(10, 40)]
    right_button = Poly(pg.Rect((370, 535), (0, 0)), 2, radius=0.5, vertices=right_button_vertices)


    lighthouses_col = [Circle(pg.Rect((230, 230), (0, 0)), 3, radius=30, body_type=pm.Body.KINEMATIC),
                        Circle(pg.Rect((375, 230), (0, 0)), 3, radius=30, body_type=pm.Body.KINEMATIC),
                            Circle(pg.Rect((300, 230), (0, 0)), 3, radius=30, body_type=pm.Body.KINEMATIC)]


    def get_collisions():

        body = pm.Body(body_type=pm.Body.STATIC)
        segments = [body]

        with open(collisions_file , "r") as file:
            data = file.read()
            obj = loads(data)

            for collision in obj:
                segments.append(pm.Segment(
                    body, (collision["x0"], collision["y0"]), (collision["x1"], collision["y1"]), radius=5))


        return segments

    space.add(*get_collisions())
    space.add(ball_.body, ball_.shape)
    space.add(left_button.body, left_button.shape)
    space.add(right_button.body, right_button.shape)

    [space.add(light.body, light.shape) for light in lighthouses_col]

    button_coord = [ { "a": 255, "b": 840, "c": 50, "d": 50 },
                        { "a": 290, "b": 840, "c": -60, "d": 60 } ]

    def create_static_lines_button():

        button1_vertices = [(0, 0), (button_coord[0]["c"], button_coord[0]["d"])]
        button1 = Poly(pg.Rect((200, 790), (0, 0)), 4, radius=10, vertices=button1_vertices)

        button2_vertices = [(0, 0), (button_coord[1]["c"], button_coord[1]["d"])]
        button2 = Poly(pg.Rect((360, 780), (0, 0)), 4, radius=10, vertices=button2_vertices)

        return [button1.body, button1.shape, button2.body, button2.shape]


    # 1 -> ball 
    # 3 -> lightsouse
    space.add_collision_handler(1, 3).post_solve = post_solve_lighthouse_ball

    done = False
    while not done:

        pg.draw.line(screen, YELLOW, (0, 0), (SCREEN_WIDTH, 0), width=25)   
        pg.draw.line(screen, YELLOW, (0, 0), (0, SCREEN_HEIGHT), width=25)
        pg.draw.line(screen, YELLOW, (0, SCREEN_HEIGHT),
                     (SCREEN_WIDTH, SCREEN_HEIGHT), width=25)
        pg.draw.line(screen, YELLOW, (SCREEN_WIDTH, 0),
                     (SCREEN_WIDTH, SCREEN_HEIGHT), width=25)
        pg.draw.line(screen, YELLOW, (SCREEN_WIDTH - 60, 750), (SCREEN_WIDTH, 750), width=20)

        buttons_lines = create_static_lines_button()
        space.add(*buttons_lines)
        
        pg.draw.line(screen, RED , (200, 790), (button_coord[0]["a"], button_coord[0]["b"]), width=20)
        pg.draw.line(screen, RED , (360, 780), (button_coord[1]["a"], button_coord[1]["b"]), width=20)


        for event in pg.event.get():

            if event.type == pg.QUIT:
                done = True

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    done = True

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
        
            if button_coord[0]["b"] >= 750:
                button_coord[0]["b"] -= 20
                button_coord[0]["d"] -= 20

        else:

            if button_coord[0]["b"] <= 830:
                button_coord[0]["b"] += 20
                button_coord[0]["d"] += 20

        if keys[pg.K_RIGHT]:
        
            if button_coord[1]["b"] >= 750:
                button_coord[1]["b"] -= 20
                button_coord[1]["d"] -= 20

        else:

            if button_coord[1]["b"] <= 830:
                button_coord[1]["b"] += 20
                button_coord[1]["d"] += 20
        

        screen.blit(sand_top.image, sand_top.rect)
        screen.blit(sand_bottom.image, sand_bottom.rect)
        screen.blit(border_top.image, border_top.rect)
        screen.blit(border_bottom.image, border_bottom.rect)
        screen.blit(pinball_bar.image, pinball_bar.rect)
        screen.blit(pinball_small_bar.image, pinball_small_bar.rect)
        screen.blit(buttons.image, buttons.rect)
        screen.blit(lighthouses.image, lighthouses.rect)

        ball.image = ball_.rotate(ball.rotate_image)
        screen.blit(ball.image, (ball_.body.position.x - ball.rect.w/2, ball_.body.position.y - ball.rect.h/2))

        pg.draw.circle(screen, WHITE, ball_.body.position, radius=10)

        if ball_.body.position.y > 735 and ball_.body.position.x == 570:
            ball_.body.apply_impulse_at_local_point((0, -1500), (0, 0)) # Init game


        label = font.render(
            f"SCORE: {ball_.shape.score}", 10, BLACK)
        screen.blit(label, (10, SCREEN_HEIGHT - 30))

        space.step(space_step)        
        pg.display.flip()

        space.remove(*buttons_lines)
        screen.fill(BLACK) # Clear
        

        if ball_.body.position.y > 985:
            screen.blit(alpha_bg, (0, 0))
            label = font.render(
                "GAME OVER", 1, YELLOW)
            screen.blit(label, (SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2.5))
            
        clock.tick(60) # FPS

if __name__ == "__main__":
    sys.exit(main())
