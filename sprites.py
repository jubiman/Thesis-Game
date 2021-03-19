import pygame
from pygame.locals import *
from settings import *
import assets


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image = pygame.transform.scale(assets.get_asset_from_name(game.graphics, 'player1').image, (64, 64))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(x, y) * TILESIZE

    def get_keys(self):
        self.vel = pygame.math.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.vel.x = -PLAYERSPEED
        if keys[K_d]:
            self.vel.x = PLAYERSPEED
        if keys[K_w]:
            self.vel.y = -PLAYERSPEED
        if keys[K_s]:
            self.vel.y = PLAYERSPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

    def collide_with_walls(self, d):
        if d == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if d == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pygame.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        self.image = pygame.transform.scale(assets.get_asset_from_name(game.graphics, "wall1").image, (64, 64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
