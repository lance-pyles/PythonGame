# Simple pygame program

import random
import pygame
from pygame.constants import K_ESCAPE, KEYDOWN
import time
import asyncio
import datetime
from datetime import timedelta
from datetime import datetime
from direction import Direction

cell_size: int = 32
game_day: int = 1
debug: bool = False
side_menu: bool = False
draw_grid: bool = False

side_columns: int = 6
debug_rows: int = 2

game_columns: int = 21
game_rows: int = 19
current_map: map



display_columns: int  = game_columns if not side_menu else game_columns + side_columns
display_rows: int = game_rows if not debug else game_rows + debug_rows

x_display_res: int = display_columns * cell_size
y_display_res: int = display_rows * cell_size

x_game_res: int = game_columns * cell_size
y_game_res: int = game_rows * cell_size

screen = pygame.display.set_mode([x_display_res, y_display_res])

datetime_object = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 6, 0, 0)

class map():
     
     tiles: list[list[str]]
     column_offset: int = 0
     row_offset: int = 0
     door_location: tuple[int, int] = (0, 0)
     
     def __init__(self, columns, rows):
     
          self.columns = columns          
          self.rows = rows
     
class game_object():
     
     def __init__(self, width, height, column, row):
     
          self.width = width          
          self.height = height
          self.column = column
          self.row = row

class cursor():
     
     x: int = -1
     y: int = -1

     def draw(self):
          pygame.draw.circle(screen, (244, 111, 111), (self.x, self.y), 5) 
     
     @property
     def column(self): 

         return (int)(self.x / cell_size) + 1 if self.x > 1 else -1
     
     @property
     def row(self): 

         return (int)(self.y / cell_size) + 1 if self.x > 1 else -1
     
class player():
     

     
     has_moved_on_map: bool
     walk_count = 0
     is_inside = 0
     
     old_column: int = -1
     old_row: int = -1
     __walkDown =  [pygame.image.load('foxDown1.png'), pygame.image.load('foxDown2.png'), pygame.image.load('foxDown3.png'), pygame.image.load('foxDown4.png'), pygame.image.load('foxDown5.png'), pygame.image.load('tile009.png'), pygame.image.load('tile010.png'), pygame.image.load('tile011.png')]
     __walkLeft =  [pygame.image.load('tile012.png'), pygame.image.load('tile013.png'), pygame.image.load('tile014.png'), pygame.image.load('tile015.png'), pygame.image.load('tile016.png'), pygame.image.load('tile017.png'), pygame.image.load('tile018.png'), pygame.image.load('tile019.png')]
     __walkRight = [pygame.image.load('tile020.png'), pygame.image.load('tile021.png'), pygame.image.load('tile022.png'), pygame.image.load('tile023.png'), pygame.image.load('tile024.png'), pygame.image.load('tile025.png'), pygame.image.load('tile026.png'), pygame.image.load('tile027.png')]
     __walkUp =    [pygame.image.load('tile028.png'), pygame.image.load('tile029.png'), pygame.image.load('tile030.png'), pygame.image.load('tile031.png'), pygame.image.load('tile032.png'), pygame.image.load('tile033.png'), pygame.image.load('tile034.png'), pygame.image.load('tile035.png')]
     
     width = 16
     height = 16
     current_sprite = __walkDown[0]
     direction: Direction =  Direction.DOWN
     
     def __init__(self, column, row):
     
          self.column = column          
          self.row = row
     
     def moveUp(self, game_map):
          global map_row_offset
          self.current_sprite = self.__walkUp[self.walk_count % 7]
          self.direction = Direction.UP
          new_row =  max(self.row - 1, 1)
          if 1 == 1:
               if game_map.tiles[new_row - 1 + current_map.row_offset ][self.column - 1 + current_map.column_offset] in ('G', 'I', 'D') and not game_map.tiles[self.row - 1 + current_map.row_offset ][self.column - 1 + current_map.column_offset] in ('D'):
                    if new_row != self.row:
                         self.old_row = self.row
                         self.row = new_row
                         self.walk_count = self.walk_count + 1 #if self.walk_count < 7 else 0
                         self.has_moved_on_map = True
                    else:
                         if game_rows - current_map.row_offset < current_map.rows:
                              current_map.row_offset -= 1   
                              self.walk_count += 1
                    
     def moveRight(self, game_map):
          global map_column_offset
          self.current_sprite = self.__walkRight[self.walk_count % 7]
          self.direction = Direction.RIGHT
          new_column = min(self.column + 1, game_columns)
          if 1 == 1:
               if game_map.tiles[self.row - 1 + current_map.row_offset][new_column - 1 + current_map.column_offset] in ('G', 'I') and not game_map.tiles[self.row - 1 + current_map.row_offset][self.column - 1 + current_map.column_offset] in ('X', 'D'):
                    if new_column != self.column:
                         self.old_column = self.column
                         self.column = new_column
                         self.walk_count = self.walk_count + 1 #if self.walk_count < 7 else 0
                         self.has_moved_on_map = True
                    else:
                         if game_columns + current_map.column_offset < current_map.columns:
                              current_map.column_offset += 1
                              self.walk_count += 1
                         
                    
     def moveDown(self, game_map):
          global map_row_offset
          self.current_sprite = self.__walkDown[self.walk_count % 7]
          self.direction = Direction.DOWN
          new_row = min(self.row + 1, game_rows)
          if 1 == 1:
               if game_map.tiles[new_row - 1 + current_map.row_offset ][self.column - 1 + current_map.column_offset] in ('G', 'I', 'X') and not game_map.tiles[self.row - 1 + current_map.row_offset][self.column - 1 + current_map.column_offset] in ('X'):
                    if new_row != self.row:
                         self.old_row = self.row
                         self.row = new_row
                         self.walk_count = self.walk_count + 1 #if self.walk_count < 7 else 0
                         self.has_moved_on_map = True
                    else:
                         if game_rows + current_map.row_offset < current_map.rows:
                              current_map.row_offset += 1 
                              self.walk_count += 1

     def moveLeft(self, game_map):
          global map_column_offset
          self.current_sprite = self.__walkLeft[self.walk_count % 7]
          self.direction = Direction.LEFT
          new_column = max(self.column - 1, 1)
          if 1 == 1:
               if game_map.tiles[self.row - 1 + current_map.row_offset][new_column - 1 + current_map.column_offset] in ('G', 'I') and not game_map.tiles[self.row - 1 + current_map.row_offset][self.column - 1 + current_map.column_offset] in ('X', 'D'):
                    if new_column != self.column:
                         self.old_column = self.column
                         self.column = new_column
                         self.walk_count = self.walk_count + 1 #if self.walk_count < 7 else 0
                         self.has_moved_on_map = True
                    else:
                         if game_columns - current_map.column_offset < current_map.columns:
                              current_map.column_offset -= 1
                              self.walk_count += 1
     @property
     def x(self): 

         return ((self.column - 1) * self.width * 2)
     
     @property
     def y(self): 

         return ((self.row - 1) * self.height * 2)

     def draw(self, screen):

          screen.blit(self.current_sprite, (self.x, self.y))

def draw_frame(screen, fox: player, display_title: bool, pointer: cursor, night: bool):
     
     global current_map
     
     if pygame.display.get_surface().get_width() != x_display_res or pygame.display.get_surface().get_height() != y_display_res:
          
          screen = pygame.display.set_mode([x_display_res, y_display_res])
          
     # Fill the background with white
     screen.fill((255, 255, 255)) 

     #fill screen with grass
     grass = pygame.image.load('grass.png')
     trees = pygame.image.load('trees.png')
     house = [[pygame.image.load('house_back_left.png'),
              pygame.image.load('house_back_center.png'),
              pygame.image.load('house_back_right.png')],
              [pygame.image.load('house_front_left.png'),
              pygame.image.load('house_front_right.png')]]
     
     door = pygame.image.load('house_front_center.png')
     house_floor = pygame.image.load('house_floor.png')
     house_door = pygame.image.load('house_door.png')
     rotated_image = pygame.transform.rotate(house_door, 180)
     house_image: list[int, int] = [0, 0]
     for row in range(0, game_rows):
          for column in range(0, game_columns):

               if current_map.tiles[row + current_map.row_offset][column + current_map.column_offset] == 'G':
                    screen.blit(grass, (cell_size * column, cell_size * row))
               elif current_map.tiles[row + current_map.row_offset][column + current_map.column_offset] == 'T':
                    screen.blit(trees, (cell_size * column, cell_size * row))

               elif current_map.tiles[row + current_map.row_offset][column + current_map.column_offset] == 'D':
                    screen.blit(door, (cell_size * column, cell_size * row))
               elif current_map.tiles[row + current_map.row_offset][column + current_map.column_offset] == 'I':
                    screen.blit(house_floor, (cell_size * column, cell_size * row))
               elif current_map.tiles[row + current_map.row_offset][column + current_map.column_offset] == 'X':
                    screen.blit(rotated_image, (cell_size * column, cell_size * row))
               else:
                    screen.blit(house[house_image[0]][house_image[1]], (cell_size * column, cell_size * row))
                    house_image = [house_image[0], house_image[1] + 1]
                    if house_image[1] == 3:
                         house_image[1] = 0
                         house_image[0] +=1
     if pygame.mouse.get_focused():

          #draw mouse
          pos = pygame.mouse.get_pos()
           
          pointer.x = pos[0]
          pointer.y = pos[1]

          pointer.draw()
          
     else:

          pointer.x, pointer.y = (-1, -1)
     
     #draw objects

     fox.draw(screen)
          
     font = pygame.font.SysFont("Arial", 14)
     if side_menu:
          txtTime = font.render(f'Date: {datetime_object.strftime("%m/%d/%Y %I:%M:%S %p")}', True, (0, 0, 0))
          screen.blit(txtTime, (cell_size * 20, cell_size * 0))
          txtDay = font.render(f'Day: {game_day}', True, (0, 0, 0))
          screen.blit(txtDay, (cell_size * 20, cell_size * 1))
     if display_title:
          
          fontTitle = pygame.font.SysFont("Papyrus", 64, True)
          fontSubTitle = pygame.font.SysFont("Papyrus", 16, True)
     
          txtTitle = fontTitle.render(f'CozyGame v1.0', True, (244, 111, 111))
          surfaceTitle = pygame.Surface((x_game_res, txtTitle.get_height()))
          surfaceTitle.fill((111, 0, 244))
          screen.blit(surfaceTitle, (0, cell_size * 10))
          screen.blit(txtTitle, (cell_size * 1, cell_size * 10))
        
          txtStart = fontSubTitle.render(f'Press enter to start', True, (244, 111, 111))
          surfaceStart = pygame.Surface((x_game_res, txtStart.get_height()))
          surfaceStart.fill((111, 0, 244))
          screen.blit(surfaceStart, (0, cell_size * 14))
          screen.blit(txtStart, (cell_size * 1, cell_size * 14))

     if debug:
     
          # Get the current FPS
          fps: float = clock.get_fps()
          
          txtFPS = font.render(f'FPS:{"%.4f" % fps}', True, (244, 0, 0))
          surfaceFPS = pygame.Surface(txtFPS.get_size())
          surfaceFPS.fill((0, 0, 192))
          screen.blit(surfaceFPS, (cell_size * 1, cell_size * game_rows))
          screen.blit(txtFPS, (cell_size * 1, cell_size * game_rows))

          txtWalkCount = font.render(f'walk_count:{fox.walk_count}', True, (244, 0, 0))
          screen.blit(txtWalkCount, (cell_size * 1, cell_size * (game_rows + 1)))
          
          txtMouse = font.render(f'Mouse: (x:{pointer.x if pointer.x != -1 else "-"}, y:{pointer.y if pointer.y != -1 else "-"})', True, (244, 0, 0))
          screen.blit(txtMouse, (cell_size * 5, cell_size * (game_rows + 1)))
     
          txtPlayer = font.render(f'Player: (x:{fox.x}, y:{fox.y})', True, (244, 0, 0))
          screen.blit(txtPlayer, (cell_size * 5, cell_size * game_rows))

          txtPlayerColumn = font.render(f'col:{fox.column}; old col:{fox.old_column if fox.old_column != -1 else "-"}', True, (244, 0, 0))
          screen.blit(txtPlayerColumn, (cell_size * 9, cell_size * game_rows))
         
          txtMouseColumn = font.render(f'col:{pointer.column if pointer.column != -1 else "-"}', True, (244, 0, 0))
          screen.blit(txtMouseColumn, (cell_size * 9, cell_size * (game_rows + 1)))

          txtPlayerRow = font.render(f'row:{fox.row}; old row:{fox.old_row if fox.old_row != -1 else "-"}', True, (244, 0, 0))
          screen.blit(txtPlayerRow, (cell_size * 13, cell_size * game_rows))

          txtPlayerDirection = font.render(f'direction:{fox.direction}', True, (244, 0, 0))
          screen.blit(txtPlayerDirection, (cell_size * 17, cell_size * game_rows))

          txtMouseRow = font.render(f'row:{pointer.row if pointer.row != -1 else "-"}', True, (244, 0, 0))
          screen.blit(txtMouseRow, (cell_size * 13, cell_size * (game_rows + 1)))
     
     if night and not fox.is_inside:
          
          target_rect = pygame.Rect(0, 0, x_game_res, y_game_res)
          shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
          pygame.draw.polygon(shape_surf, (0, 0, 255, 127), ((0, 0), (0, y_game_res), (x_game_res, y_game_res), (x_game_res, 0)))
          screen.blit(shape_surf, target_rect)
     
     #draw a grid
     if draw_grid:
          
          pygame.draw.line(screen, (0, 0, 0), (0, 0), (0, y_game_res - 1), 1)
          pygame.draw.line(screen, (0, 0, 0), (x_game_res - 1, 0), (x_game_res - 1, y_game_res - 1), 1)
          pygame.draw.line(screen, (0, 0, 0), (0, 0), (x_game_res - 1, 0), 1)
          pygame.draw.line(screen, (0, 0, 0), (0, y_game_res - 1), (x_game_res - 1, y_game_res - 1), 1)
          
          #vertical
          for x in range(1, game_columns):
                                             
               #2 pixels wide; 1 in each tile
               pygame.draw.line(screen, (0, 0, 0), ((x * cell_size) - 1, 0), ((x * cell_size) - 1, y_game_res - 1), 2)

          #horizontal              
          for y in range(1, game_rows):  
               
               #2 pixels wide; 1 in each tile    
               pygame.draw.line(screen, (0, 0, 0), (0, ((y * cell_size) - 1)), ((x_game_res - 1), ((y * cell_size) - 1)), 2)

     # Flip the display
     pygame.display.flip()

# Create a clock object
clock = pygame.time.Clock()

def createMap(house: game_object, m: map) -> map:
     
     percent_trees: int = 1
     print('Creating map.')
     print(f'Using {percent_trees}% trees.')
     rows, cols = (m.rows, m.columns)
     arr = [['l' for i in range(0, cols)] for j in range(0, rows)]

     for row in range(0, len(arr)):
          
          for column in range(0, len(arr[0])):

               arr[row][column] = 'G' if random.randint(1, 100) > percent_trees else 'T'
     
     #no trees where the fox spawns
     arr[1][1] = 'G'      
     
     #no trees where the door is
     arr[house.row + 2][house.column + 1] = 'G'     
     m.door_location = (house.column + 2, house.row + 2)
     #place house
     #TODO: update so it cannot spawn over objects or debug row or close enough to debug row that you cannot enter

     tracker: int = 0
     for row in range(0, 2):
          for col in range(0, 3):
     
               arr[house.row + row][house.column + col] = tracker
               if row == 1 and col == 1:
                    arr[house.row + row][house.column + col] = 'D'
               else:
                    tracker += 1
     print('Map created.')      
     for x in arr:

          print(x)
          
     m.tiles = arr    
     return m
def createMapInside(house_exit: game_object, m: map) -> map:
     

     print('Creating map.')
     #print(f'Using {percent_trees}% trees.')
     rows, cols = (m.rows, m.columns)
     arr = [['l' for i in range(0, cols)] for j in range(0, rows)]
     #house: game_object = game_object(2, 3)
     for row in range(0, len(arr)):
          
          for column in range(0, len(arr[0])):

               arr[row][column] = 'I'
     
     #no trees where the fox spawns
     arr[game_rows - 1][10] = 'X'        

     print('Map created.')      
     for x in arr:

          print(x)
     m.tiles = arr    
     return m
async def main():

     global debug
     global side_menu
     global draw_grid
     
     global display_rows
     global display_columns
     global x_display_res
     global y_display_res
     global datetime_object
     global game_day
     global current_map
     
     pygame.display.set_caption('CozyGame v1.0')
     pygame.init()
     
     display_title: bool = True


     fox: player = player(2, 2)
     pointer: cursor = cursor()
     night: bool = True if datetime_object.hour >= 10 and datetime_object.hour <= 6 else False
     house: game_object = game_object(2, 3, random.randint(1, game_columns - 4), random.randint(1, game_rows - 3))
     house_exit: game_object = game_object(1, 1, 10, game_rows)
     game_map = createMap(house, map(30, 30))
     house_map = createMapInside(house_exit, map(game_columns, game_rows))
     current_map = game_map


     time_elapsed_since_last_action: int = 0
     
     # Run until the user asks to quit
     running = True
     while running:

          dt = clock.tick(30)
          time_elapsed_since_last_action += dt
          time_change = timedelta(minutes=dt/10) 
          datetime_object = datetime_object + time_change
          
          if (datetime_object.hour > 22 or datetime_object.hour < 6):
               night = True
               
          else:
               game_day = game_day + 1 if night else game_day
               night = False

               
          # Did the user click the window close button?
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    running = False
               if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                         display_title = False

                    if event.key == pygame.K_s:

                         side_menu = False if side_menu else True
                         display_columns  = game_columns if not side_menu else game_columns + side_columns
                         display_rows = game_rows if not debug else game_rows + debug_rows

                         x_display_res = display_columns * cell_size
                         y_display_res = display_rows * cell_size
                    if event.key == pygame.K_d:
                         debug = False if debug else True
                         display_columns  = game_columns if not side_menu else game_columns + side_columns
                         display_rows = game_rows if not debug else game_rows + debug_rows

                         x_display_res = display_columns * cell_size
                         y_display_res = display_rows * cell_size
                    if event.key == pygame.K_g:
                         draw_grid = False if draw_grid else True

          if time_elapsed_since_last_action > 100 and not display_title:
               
               time_elapsed_since_last_action = 0
               
               keys = pygame.key.get_pressed()
               
               if keys[pygame.K_LEFT]:                    
                    fox.moveLeft(current_map)
                         
               if keys[pygame.K_RIGHT]:       
                    fox.moveRight(current_map)

               if keys[pygame.K_UP]:
                    fox.moveUp(current_map)
                    

               if keys[pygame.K_DOWN]:
                    fox.moveDown(current_map)
                    
          if current_map.tiles[fox.row - 1 + current_map.row_offset][fox.column - 1 + current_map.column_offset] in ('D') and fox.has_moved_on_map:
               current_map = house_map
               fox.is_inside = True
               fox.column = 11
               fox.row = game_rows
               fox.has_moved_on_map = False
          elif current_map.tiles[fox.row - 1 + current_map.row_offset][fox.column - 1 + current_map.column_offset] in ('X') and fox.has_moved_on_map:
               current_map = game_map
               fox.is_inside = False
               fox.column = game_map.door_location[0] - game_map.column_offset
               fox.row = game_map.door_location[1] - game_map.row_offset
               fox.has_moved_on_map = False
               
          draw_frame(screen, fox, display_title, pointer, night)

          await asyncio.sleep(0)  # This line is critical; ensure you keep the sleep time at 0

     pygame.quit()
     

          
asyncio.run(main())