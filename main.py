import sys
import pygame
import pygame_menu
from snake import Snake
from fruit import Fruit
from config import *
from pygame.math import Vector2

class Main: 
    def __init__(self) -> None:
        self.snake = Snake()
        self.fruit = Fruit()
    
    def update(self):
        self.snake.move_snake() 
        self.check_collision()
        self.check_fail()
        
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
                
    def check_fail(self): #chequea si la vibora se encuentra outside de la pantalla
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
            #chequea que si la vibora se come el mismo muere.
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        game_close = False
        while game_close == False:
            message("Perdiste! Presiona Q para salir del juego", (213, 50, 80))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
    
    def draw_grass(self):
        grass_color = (167,209,61)
        
        for row in range(cell_number):
            if row %2 ==0:
                for col in range(cell_number):
                    if col%2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            
            else:
                for col in range(cell_number):
                    if col%2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 100)
        score_y = int(cell_size * cell_number - 100)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        comidita_rect = comidita.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(comidita_rect.left,comidita_rect.top,comidita_rect.width + score_rect.width + 20, comidita_rect.height)
        
        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(comidita,comidita_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect, 2)

main_game = Main()

def message(msg, color):
    mesg = game_font.render(msg, True, color)
    screen.blit(mesg, [cell_number * cell_size / 10, cell_number * cell_size / 2])
    
def game_start():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1,0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)        
        
        screen.fill((175,215,70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)
        
def game_menu():
    font = 'font/1up.ttf'
    mytheme = pygame_menu.Theme(
                background_color=(0, 0, 0, 0),
                title_background_color=(130, 135, 131),
                # title_font_shadow=True,
                title_font=font,
                # title_font_size=24,
                widget_font=font,
                widget_padding=25,
                )
    myimage = pygame_menu.baseimage.BaseImage(
    image_path='graficos/menu_fondo.jpg',
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    mytheme.background_color = myimage

    menu = pygame_menu.Menu('Snake Game',
                            cell_number * cell_size, 
                            cell_number * cell_size,
                            theme=mytheme)

    menu.add.button('Jugar', game_start)
    menu.add.button('Salir', pygame_menu.events.EXIT)

    menu.mainloop(screen)
    
game_menu()