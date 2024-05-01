import pygame

class Alien(pygame.sprite.Sprite):

  def __init__(self, alien_variation, x, y):
       super().__init__()

       file_path = './assets/' + alien_variation + '.png'
       self.image = pygame.image.load(file_path).convert_alpha()
       self.rect = self.image.get_rect(topleft = (x,y))

       if alien_variation == 'alien01': self.value = 300
       elif alien_variation == 'alien02': self.value = 200
       else: self.value = 100

  def update(self, direction):
      self.rect.x += direction

class Extra_Alien(pygame.sprite.Sprite):
     
     def __init__(self, side, screen_width):
       super().__init__()
       self.image = pygame.image.load('./assets/extra_alien.png'). convert_alpha()

       if side == 'right':
           x = screen_width + 50
           self.speed = -4
       else:
           x = -50
           self.speed = 4
        
        
       self.rect = self.image.get_rect(topleft = (x, 30))

     def update(self):
         self.rect.x += self.speed
  