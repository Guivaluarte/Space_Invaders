import pygame
from laser import Laser

white = (255,255,255)

class Ship(pygame.sprite.Sprite):

  def __init__(self, position, constraint, speed):
       super().__init__()

       self.image = pygame.image.load('./assets/Player.png').convert_alpha()
       self.rect = self.image.get_rect(midbottom = position)
       self.speed = speed
       self.max_x_contraint = constraint
       self.laser_ready = True
       self.laser_time = 0
       self.laser_cooldown = 700

       self.shoot_laser = pygame.sprite.Group()

  def get_input(self):
      keys = pygame.key.get_pressed()

      if keys[pygame.K_RIGHT]:
          self.rect.x += self.speed
      elif keys[pygame.K_LEFT]:
          self.rect.x -= self.speed
      if keys[pygame.K_SPACE] and self.laser_ready:
          self.shoot()
          self.laser_ready = False
          self.laser_time = pygame.time.get_ticks()

  def reload_laser(self):
      if not self.laser_ready:
          time = pygame.time.get_ticks()
          if time - self.laser_time >= self.laser_cooldown:
              self.laser_ready = True
      
  def shoot(self):
      self.shoot_laser.add(Laser(self.rect.center, -10, self.rect.bottom))


    
  def player_colision(self):
     if self.rect.left <= 0:
         self.rect.left = 0
     if self.rect.right >= self.max_x_contraint:
         self.rect.right = self.max_x_contraint

  def update(self):
     self.get_input()
     self.player_colision()
     self.reload_laser()
     self.shoot_laser.update()
