import pygame
from pygame.locals import *
from models import Asteroid, Spaceship
from utils import get_random_position, load_sprite, print_text

import serial


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.message = ""
        self.start_game_screen = True
        self.game_over_screen = False

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))
            
               # configure the serial port

        self.ser=serial.Serial(
        port='COM10',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS
        )
        self.ser.isOpen()

    def main_loop(self):
        while True:
            if self.start_game_screen:
                self._display_start_game_screen()
            elif self.game_over_screen:
                self._display_game_over_screen()
            else:
                self._handle_input()
                self._process_game_logic()
                self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _display_start_game_screen(self):
        self.screen.fill((0, 0, 0))  # Fill screen with black color
        text_start = self.font.render("Press SPACEBAR to start the game", True, (255, 255, 255))
        text_rect_start = text_start.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text_start, text_rect_start)
        pygame.display.flip()
        # Wait for 3 seconds before starting the game
        pygame.time.wait(3000)
        text_start = self.font.render("Loading", True, (255, 255, 255))
        text_rect_start = text_start.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text_start, text_rect_start)
        pygame.display.flip()
        # Wait for 3 seconds before starting the game

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.start_game_screen = False

    def _display_game_over_screen(self):
        self.screen.fill((0, 0, 0))  # Fill screen with black color
        text_game_over = self.font.render("Game Over. Press SPACEBAR to restart", True, (255, 255, 255))
        text_rect_game_over = text_game_over.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text_game_over, text_rect_game_over)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                # Reset the game
                self.reset_game()

    def reset_game(self):
        self.start_game_screen = True
        self.game_over_screen = False
        self.message = ""
        self.asteroids.clear()
        self.bullets.clear()
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))
            
    def create_serial(port):
        # configure the serial port
        ser = serial.Serial(
        port='COM4',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS
        )
        ser.isOpen()

    def _handle_input(self):
        # Check for keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

        # Read data from serial port with timeout
        instruction = self.ser.readline().decode().strip()
        if instruction:
            coordinates = instruction.split()
            if len(coordinates) < 2:
                print("Error: Insufficient coordinates in the instruction:", instruction)
                return  # Exit the function if there are not enough coordinates
            x, y = map(float, coordinates)
            # Update spaceship position based on the received coordinates
            if (x, y) == (33, 16):  # Going forward
                self.spaceship.move_up()
                print(x,y)
            elif (x, y) == (0, 16):  # Going backward
                self.spaceship.move_down()
                print(x,y)
            elif (x, y) == (16, 33):  # Going right
                self.spaceship.move_right()
                print(x,y)
            elif (x, y) == (16, 0):  # Going left
                self.spaceship.move_left()
                print(x,y)



    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "You lost!"
                    self.game_over_screen = True
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.message = "You won!"
            self.game_over_screen = True

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

