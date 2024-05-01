import pygame

class Laser(pygame.sprite.Sprite):
  def __init__(self, position, laser_speed , screen_height):
    super().__init__()
    self.image = pygame.Surface((4,20))
    self.image.fill('white')
    self.rect = self.image.get_rect(center = position)
    self.laser_speed = laser_speed
    self.screen_height_constraint = screen_height
  
  def destroy_laser(self):
    if self.rect.y <= -50 or self.rect.y >= self.screen_height_constraint + 50:
      self.kill()

  def update(self):
    self.rect.y += self.laser_speed
    self.destroy_laser()



