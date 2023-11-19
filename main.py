# Simple pygame program
import random
import pygame
from pygame.constants import K_ESCAPE, KEYDOWN
import time
import asyncio

cell_size: int = 32
debug: bool = True
debug_rows: int = 22
display_rows: int = 20
rows: int = display_rows if not debug else debug_rows
columns: int  = 20
x_res: int = columns * cell_size
y_res: int = rows * cell_size
screen = pygame.display.set_mode([x_res, y_res])

class player():
     walk_count = 0
     x: int = 0
     y: int = 0
     old_column: int = 0
     old_row: int = 0
     __walkDown = [pygame.image.load('tile004.png'), pygame.image.load('tile005.png'), pygame.image.load('tile006.png'), pygame.image.load('tile007.png'), pygame.image.load('tile008.png'), pygame.image.load('tile009.png'), pygame.image.load('tile010.png'), pygame.image.load('tile011.png')]
     __walkUp = [pygame.image.load('tile028.png'), pygame.image.load('tile029.png'), pygame.image.load('tile030.png'), pygame.image.load('tile031.png'), pygame.image.load('tile032.png'), pygame.image.load('tile033.png'), pygame.image.load('tile034.png'), pygame.image.load('tile035.png')]
     __walkRight = [pygame.image.load('tile020.png'), pygame.image.load('tile021.png'), pygame.image.load('tile022.png'), pygame.image.load('tile023.png'), pygame.image.load('tile024.png'), pygame.image.load('tile025.png'), pygame.image.load('tile026.png'), pygame.image.load('tile027.png')]
     __walkLeft = [pygame.image.load('tile012.png'), pygame.image.load('tile013.png'), pygame.image.load('tile014.png'), pygame.image.load('tile015.png'), pygame.image.load('tile016.png'), pygame.image.load('tile017.png'), pygame.image.load('tile018.png'), pygame.image.load('tile019.png')]
     width = 16
     height = 16
     current_sprite = __walkDown[0]
     def __init__(self, column, row):
     
          self.column = column
          
          self.row = row
     
     def moveUp(self, map_exit):
          new_row =  max(self.row - 1, 1)
          if map_exit.moveAllowed(self.column, new_row, self.column, self.row):
               if new_row != self.row:
                    self.old_row = self.row
                    self.row = new_row
                    self.walk_count = self.walk_count + 1 if self.walk_count < 7 else 0
                    self.current_sprite = self.__walkUp[self.walk_count]
                    
     def moveRight(self, map_exit):
          new_column = min(self.column + 1, columns)
          if map_exit.moveAllowed(new_column, self.row, self.column, self.row):
               if new_column != self.column:
                    self.old_column = self.column
                    self.column = new_column
                    self.walk_count = self.walk_count + 1 if self.walk_count < 7 else 0
                    self.current_sprite = self.__walkRight[self.walk_count]
                    
     def moveDown(self, map_exit):
          new_row = min(self.row + 1, rows if not debug else rows - 2)
          if map_exit.moveAllowed(self.column, new_row, self.column, self.row):
               if new_row != self.row:
                    self.old_row = self.row
                    self.row = new_row
                    self.walk_count = self.walk_count + 1 if self.walk_count < 7 else 0
                    self.current_sprite = self.__walkDown[self.walk_count]
                    
     def moveLeft(self, map_exit):
          
          new_column = max(self.column - 1, 1)
          if map_exit.moveAllowed(new_column, self.row, self.column, self.row):
               if new_column != self.column:
                    self.old_column = self.column
                    self.column = new_column
                    self.walk_count = self.walk_count + 1 if self.walk_count < 7 else 0
                    self.current_sprite = self.__walkLeft[self.walk_count]

     @property
     def x(self): 

         return ((self.column - 1) * self.width * 2)
     
     @property
     def y(self): 

         return ((self.row - 1) * self.height * 2)

     def draw(self, screen):


          screen.blit(self.current_sprite, (self.x, self.y))

class exit():
     
     x: int = 0
     y: int = 0
     cells = []

     
     def __init__(self, column, row):
          
          self.column = column
          self.row = row
      
     @property
     def hitbox(self):
          self.cells.clear()
          self.cells.append((self.column - 1, self.row))
          self.cells.append((self.column, self.row))
          self.cells.append((self.column + 1, self.row))
          self.cells.append((self.column - 1, self.row - 1))
          self.cells.append((self.column, self.row - 1))
          self.cells.append((self.column + 1, self.row - 1))
          return self.cells
          
     @property
     def x(self): 

         return (self.column - 1) * cell_size
     
     @property
     def y(self): 

         return (self.row - 1) * cell_size
    
     def moveAllowed(self, column, row, old_column, old_row):

          #moving up into the exit is allowed
          if old_row == row + 1 and self.row == row and self.column == column:
               return True

          #moving down from the exit is allowed
          if old_row == self.row and old_column == self.column:
               if row == self.row + 1:
                    return True
               return False

          #if they won't hit the exit the move is allowed
          for column2, row2 in self.hitbox:
               
               if row2 == row and column2 == column:
     
                    return False

          return True
     
     def draw (self, screen):
          exitImage3 = pygame.image.load('house_front_left.png')
          exitImage = pygame.image.load('house_front_center.png')
          exitImage4 = pygame.image.load('house_front_right.png')
          exitImage5 = pygame.image.load('house_back_left.png')
          exitImage2 = pygame.image.load('house_back_center.png')
          exitImage6 = pygame.image.load('house_back_right.png')
          screen.blit(exitImage3, (self.x - cell_size, self.y))
          screen.blit(exitImage, (self.x, self.y))
          screen.blit(exitImage4, (self.x + cell_size, self.y))
          screen.blit(exitImage5, (self.x - cell_size, self.y - cell_size))
          screen.blit(exitImage2, (self.x, self.y - cell_size))  
          screen.blit(exitImage6, (self.x + cell_size, self.y - cell_size))


# Create a clock object
clock = pygame.time.Clock()

async def main():

     global debug


     pygame.init()
     

     draw_grid: bool = False

     display_title: bool = True

     fox: player = player(1, 1)
     
     
     
     #TODO: update so it cannot spawn over objects or debug row
     map_exit: exit = exit(max(random.randrange(1, columns - 1, 1), 2), max(random.randrange(1, rows - 1, 1), 2))
     
    # level_in_progress: bool = True
     time_elapsed_since_last_action: int = 0
     # Run until the user asks to quit
     running = True
     while running:
          dt = clock.tick(60)
          time_elapsed_since_last_action += dt

          # Did the user click the window close button?
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False
               if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                         display_title = False
                    if event.key == pygame.K_d and pygame.key.get_mods() and pygame.KMOD_CTRL:
                         debug = False if debug else True

          if time_elapsed_since_last_action > 100 and not display_title:
               
               time_elapsed_since_last_action = 0
               
               keys = pygame.key.get_pressed()
               
               if keys[pygame.K_LEFT]:                    
                    fox.moveLeft(map_exit)
                         
               if keys[pygame.K_RIGHT]:       
                    fox.moveRight(map_exit)

               if keys[pygame.K_UP]:
                    fox.moveUp(map_exit)
                    

               if keys[pygame.K_DOWN]:
                    fox.moveDown(map_exit)
 


          draw_frame(screen, map_exit, fox, display_title, draw_grid)


          
          await asyncio.sleep(0)  # This line is critical; ensure you keep the sleep time at 0

     pygame.quit()
     
def draw_frame(screen, map_exit: exit, fox: player, display_title: bool, draw_grid: bool):
     
     global rows
     global columns
     global x_res
     global y_res

     
     rows = 20 if not debug else 22
     columns  = 20
     x_res = columns * cell_size
     y_res = rows * cell_size
     if pygame.display.get_surface().get_width() != x_res or pygame.display.get_surface().get_height() != y_res:
          
          screen = pygame.display.set_mode([x_res, y_res])
     # Fill the background with white
     screen.fill((255, 255, 255))  
     #fill screen with grass
     grass = pygame.image.load('grass.png')

     for column in range(0, columns):
          for row in range(0, rows if not debug else rows - 2):
               screen.blit(grass, (cell_size * column, cell_size * row))
                    
     #draw mouse
     pos = pygame.mouse.get_pos() 
     pygame.draw.circle(screen, (0, 255, 0), pos, 5) 
     
     #draw objects
     map_exit.draw(screen)
     fox.draw(screen)

     mouse_column: int = (int)(pos[0] / cell_size) + 1
     mouse_row: int = (int)(pos[1] / cell_size) + 1
     
     font = pygame.font.SysFont("Arial", 14)
     font2 = pygame.font.SysFont("Papyrus", 30, True)

     if display_title:
          
          txtTitle = font2.render(f'CozyGame v1.0', True, (244, 0, 0))
          screen.blit(txtTitle, ((x_res - txtTitle.get_width()) // 2, (((display_rows * cell_size) - txtTitle.get_height()) // 2) - 16))
          
          txtStart = font.render(f'Press enter to start', True, (244, 0, 0))
          screen.blit(txtStart, ((x_res - txtStart.get_width()) // 2, (((display_rows * cell_size) - txtStart.get_height()) // 2) + 16))
      
     # Get the current FPS
     fps = clock.get_fps()
     
     if debug:

          txtFPS = font.render(f'FPS:{"%.4f" % fps}', True, (244, 0, 0))
          screen.blit(txtFPS, (50, 640))
          
          txtMouse = font.render(f'Mouse: (x:{pos[0]}, y:{pos[1]})', True, (244, 0, 0))
          screen.blit(txtMouse, (200, 656))
     
          txtPlayer = font.render(f'Player: (x:{fox.x}, y:{fox.y})', True, (244, 0, 0))
          screen.blit(txtPlayer, (200, 640))

          txtPlayerColumn = font.render(f'column:{fox.column}; old column:{fox.old_column if fox.old_column != 0 else "n/a"}', True, (244, 0, 0))
          screen.blit(txtPlayerColumn, (350, 640))
         
          txtMouseColumn = font.render(f'column:{mouse_column}; old column:{-1}', True, (244, 0, 0))
          screen.blit(txtMouseColumn, (350, 656))

          txtPlayerRow = font.render(f'row:{fox.row}; old row:{fox.old_row if fox.old_row != 0 else "n/a"}', True, (244, 0, 0))
          screen.blit(txtPlayerRow, (500, 640))

          txtMouseColumn = font.render(f'row:{mouse_row}; old row:{-1}', True, (244, 0, 0))
          screen.blit(txtMouseColumn, (500, 656))
     
          txtsurf55 = font.render(f'walkCount:{fox.walk_count}', True, (244, 0, 0))
          screen.blit(txtsurf55,(650, 640))
          
          #draw a grid
          if draw_grid:
               
               for x in range(x_res):
                    
                    if x % (fox.width * 2) == 0:
                         
                         pygame.draw.line(screen, (0, 0, 0), (0, x), (y_res, x))
                         
               for y in range(y_res):
                    
                    if y % (fox.height * 2) == 0:
                         
                         pygame.draw.line(screen, (0, 0, 0), (y, 0), (y, x_res))

     # Flip the display
     pygame.display.flip()
          
asyncio.run(main())