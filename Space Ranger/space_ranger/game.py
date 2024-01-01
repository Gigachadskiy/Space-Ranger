import pygame

from models import Asteroid, Spaceship
from utils import get_random_position, load_sprite, print_text

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 844

class SpaceRanger:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self._init_game()

    def _init_game(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.restart_button = pygame.Rect(300, 400, 200, 50)
        self.restart_button_color = (0, 128, 255)
        self.restart_button_text_color = (255, 255, 255)
        self.restart_button_font = pygame.font.SysFont('Corbel', 35)
        self.restart_button_text = self.restart_button_font.render("Restart", True, self.restart_button_text_color)
        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        self.score = 0

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Ranger")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()
        mods = pygame.key.get_mods()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT] and not mods & pygame.KMOD_CTRL:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT] and not mods & pygame.KMOD_CTRL:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
        self._handle_restart_button()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "You lost!"
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    self.score += 1
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.message = "You won!"

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            if self.spaceship is None:
                pygame.draw.rect(self.screen, (0, 128, 255), self.restart_button)
                self.screen.blit(
                    self.restart_button_text,
                    (self.restart_button.x + 50, self.restart_button.y + 15),
                )
                game_over_message = f"Score : {self.score}"
                print_text(self.screen, game_over_message, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _handle_restart_button(self):
        mouse_pos = pygame.mouse.get_pos()
        click, _, _ = pygame.mouse.get_pressed()

        if self.restart_button.collidepoint(mouse_pos) and click:
            self._init_game()
            self.message = ""  

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

if __name__ == "__main__":
    space_rocks_game = SpaceRanger()
    space_rocks_game.main_loop()
