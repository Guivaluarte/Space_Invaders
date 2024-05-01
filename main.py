import pygame, sys
from Player import Ship
import obstacle
from aliens import Alien, Extra_Alien
from random import choice, randint
from laser import Laser


class Game:
   def __init__(self):

      player_sprite = Ship((width/2, height - 30), width, 10)
      self.player = pygame.sprite.GroupSingle(player_sprite)

      self.lives = 3
      self.live_display = pygame.image.load('./assets/Player.png').convert_alpha()
      self.live_x_position = width - (self.live_display.get_size()[0])
      self.score = 0
      self.font = pygame.font.Font('./assets/font/Silkscreen/slkscr.ttf',20)

      self.shape = obstacle.shape
      self.block_size = 6
      self.blocks = pygame.sprite.Group()
      self.obstacles_number = 4
      self.obstacles_x_positions = [num * (width/ self.obstacles_number) for num in range(self.obstacles_number)]
      self.create_multiple_obstacles(*self.obstacles_x_positions, x_start = width/15, y_start = 480)

      self.alien = pygame.sprite.Group()
      self.alien_laser = pygame.sprite.Group()
      self.alien_setup(rows = 6, collums = 8)
      self.alien_direction = 1

      self.extra_alien = pygame.sprite.GroupSingle()
      self.extra_alien_spawn_time = randint(400, 800)
   

   def create_obstacle(self, x_start, y_start, offset_x):
      for row_index, row in enumerate(self.shape):
         for collum_index, collum  in enumerate(row):

            if collum == 'x':
               x = x_start + collum_index * self.block_size + offset_x
               y = y_start +  row_index * self.block_size

               block = obstacle.Obstacle( self.block_size,(255,255,255), x , y)

               self.blocks.add(block)

   def create_multiple_obstacles(self, *offset, x_start, y_start,):

      for offset_x in offset:
         self.create_obstacle(x_start, y_start,offset_x)

   def alien_setup(self, rows, collums, x_distance = 60, y_distance = 48, x_offset = 80, y_offset = 60):
      for row_index, row in enumerate(range(rows)):
         for collum_index, collum  in enumerate(range(collums)):
            x = collum_index * x_distance + x_offset
            y = row_index * y_distance + y_offset

            if row_index == 0: alien_sprite = Alien('alien01', x, y)
            elif 1 <= row_index <=2: alien_sprite = Alien('alien02', x, y)
            else: alien_sprite = Alien('alien03', x, y)

            self.alien.add(alien_sprite)

   def alien_check_position(self):
      all_aliens = self.alien.sprites()

      for alien in all_aliens:
         if alien.rect.right >= width:
            self.alien_direction = -1
            self.aliens_down(2)

         elif alien.rect.left <= 0:
            self.alien_direction = 1
            self.aliens_down(2)

   def aliens_down(self, distance):
      if self.alien:
         for alien in self.alien.sprites():
            alien.rect.y += distance
   
   def aliens_ai(self):
      if self.alien.sprites():
         random_alien =  choice(self.alien.sprites())
         alien_laser_aprite = Laser( random_alien.rect.center, 6 , height)
         self.alien_laser.add(alien_laser_aprite)

   def extra_alien_timer(self):
      self.extra_alien_spawn_time -= 1
      if self.extra_alien_spawn_time <= 0:
         self.extra_alien.add(Extra_Alien(choice(['right, left']), width))
         self.extra_alien_spawn_time = randint(400, 800)

   
   
   def check_colisions(self):

      if self.player.sprite.shoot_laser:
         for laser in self.player.sprite.shoot_laser:

            if pygame.sprite.spritecollide(laser,self.blocks,True):
               laser.kill()
            

            aliens_hit = pygame.sprite.spritecollide(laser,self.alien,True)

            if aliens_hit:
               for alien in aliens_hit:
                  self.score += alien.value
               laser.kill()
            
            if pygame.sprite.spritecollide(laser,self.extra_alien,True):
               self.score += 600
               laser.kill()
               
      if self.alien_laser:
         for laser in self.alien_laser:
            if pygame.sprite.spritecollide(laser,self.blocks,True):
               laser.kill()

            if pygame.sprite.spritecollide(laser,self.player,False):
               laser.kill()
               self.lives -= 1
               if self.lives <= 0:
                   pygame.quit()
                   sys.exit()


      if self.alien:
         for alien in self.alien:
             pygame.sprite.spritecollide(alien,self.blocks,True)

             if pygame.sprite.spritecollide(alien,self.player,False):
                pygame.quit()
                sys.exit()
                
   def show_lives(self):
      for live in range( self.lives -1):
         x = self.live_x_position + (live * self.live_display.get_size()[0] -  40)
         screen.blit(self.live_display, (x, 8))
              
   def display_score(self):
      score_display = self.font.render(f'score: {self.score}', False,'white')
      score_rect = score_display.get_rect(topleft = (10,0))
      screen.blit(score_display,score_rect)

   def victory_message(self):
      if not self.alien.sprites():
         victory_display = self.font.render('You Won!!!', False, 'white')
         victory_rect = victory_display.get_rect(center = (width/2, height/2))
         screen.blit(victory_display, victory_rect)

   def run (self):
      self.player.update()

    
      self.check_colisions()

      self.alien.update(self.alien_direction)
      self.alien_check_position()
      self.alien_laser.update()
      self.extra_alien_timer()
      self.extra_alien.update()

      self.player.sprite.shoot_laser.draw(screen)
      self.player.draw(screen)

      self.blocks.draw(screen)

      self.alien.draw(screen)
      self.alien_laser.draw(screen)
      self.extra_alien.draw(screen)
      self.show_lives()
      self.display_score()
      self.victory_message()








#basic game setup
pygame.init()
width = 600
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("Space invaders")
game = Game()

ALIENLASER = pygame.USEREVENT + 1
pygame.time.set_timer(ALIENLASER,600)

running = True
#Main game loop
while running:
   # Handle screen closing 
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()
      
      if event.type == ALIENLASER:
         game.aliens_ai()

   

   screen.fill((30,30,30))
   game.run()

   pygame.display.flip()
   clock.tick(60)

