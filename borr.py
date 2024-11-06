import pygame
import pytmx

# variables globales
WIDTH_SCREEN, HEIGHT_SCREEN = 272, 208
PLAYER_SIZE = 16
POSITION_PLAYER_X, POSITION_PLAYER_Y = 32, 32
GAME_SCALE = 2
FREE_TILE = 0
NONE_TILE = 0
PLAYER_SPEED = PLAYER_SIZE
WHITE = (0, 0, 0)
PATH_STAGE1_MAP = "TiledMap/Stage1/Stage1.tmx"
PATH_PLAYER_SPRITE= "Sprites/bomberman_main.png"
PATH_PLAYER_DOWN="Sprites/bomberman_down.png"
PATH_BLOCK_SPRITE= "Sprites/block_town.png"
BLOCK_BOMB="sprites/bomb_sprite.png"

class Player:
    def _init_(self, x, y, size, speed, sprite, game_scale):
        self.posX = x
        self.posY = y
        self.size = size
        self.speed = speed
        self.sprite = pygame.image.load(sprite)
        # Escala la imagen al tamaño del jugador
        self.scaled_player_sprite = pygame.transform.scale(self.sprite, (game_scale * size, size * game_scale))

    def move(self, movement_x, movement_y):
        self.posX += movement_x     #offset_x
        self.posY += movement_y 

    def draw(self, game_window, scale_game):
        scaled_size = int(self.size * scale_game)
        scaled_player_rect = pygame.Rect(self.posX * scale_game, self.posY * scale_game, scaled_size, scaled_size)
        # Dibuja el sprite en pantalla
        game_window.blit(self.scaled_player_sprite, scaled_player_rect)


class Block:
    collision_block = None
    def _init_(self, x, y, size, sprite, game_scale):
        self.posX = x
        self.posY = y
        self.size = size
        self.sprite = pygame.image.load(sprite)
        self.scaled_block_sprite = pygame.transform.scale(self.sprite, (game_scale * size, size * game_scale))

    def draw(self, game_window, scale_game):
        scaled_size = int(self.size * scale_game)
        scaled_block_rect = pygame.Rect(self.posX * scale_game, self.posY * scale_game, scaled_size, scaled_size)
        game_window.blit(self.scaled_block_sprite, scaled_block_rect)
        self.collision_block  = scaled_block_rect  
class Bomb:
    def _init_(self, x, y, size, sprite, game_scale, timer=2):
        self.posX = x
        self.posY = y
        self.size = size
        self.timer = timer
        self.exploded = False
        self.sprite = pygame.image.load(sprite)
        self.scaled_bomb_sprite = pygame.transform.scale(self.sprite, (game_scale * size, size * game_scale))

    def draw(self, game_window, scale_game):
        scaled_size = int(self.size * scale_game)
        bomb_rect = pygame.Rect(self.posX * scale_game, self.posY * scale_game, scaled_size, scaled_size)
        game_window.blit(self.scaled_bomb_sprite, bomb_rect.topleft)

    def update(self):
        # Disminuye el temporizador y devuelve True si llega a 0
        print(self.timer)
        self.timer -= 1
        if self.timer <=0:
            self.exploted = True
        #return self.timer <= 0
                
    

class GameEngine:
    def _init_(self, width, height, GAME_SCALE, player_size, player_speed):
        pygame.init()
        self.screen = pygame.display.set_mode((width * GAME_SCALE, height * GAME_SCALE))
        self.player = Player(POSITION_PLAYER_X, POSITION_PLAYER_Y, player_size, player_speed, PATH_PLAYER_SPRITE, GAME_SCALE)
        self.game_scale = GAME_SCALE
        # Obtener las capas del mapa
        self.tmx_map = pytmx.load_pygame(PATH_STAGE1_MAP)
        self.terrain_layer = self.tmx_map.get_layer_by_name("Terrain")
        self.wall_layer = self.tmx_map.get_layer_by_name("Wall")
        self.block_layer = self.tmx_map.get_layer_by_name("Block")
        self.tile_width = self.tmx_map.tilewidth   
        self.tile_height = self.tmx_map.tileheight 
        # Lista para almacenar instancias de Block
        self.blocks = []
        self.bombs = []  
        # Crear objetos Block en las posiciones de la capa Wall
        for y, row in enumerate(self.block_layer.data):
            for x, ID_tile in enumerate(row):
                if ID_tile != NONE_TILE:
                    block_size = self.tile_width  # Ajusta el tamaño según tus necesidades
                    block_sprite_path = PATH_BLOCK_SPRITE
                    block = Block(x * self.tile_width, y * self.tile_height, block_size, block_sprite_path, GAME_SCALE)
                    self.blocks.append(block)
    
    def can_move_to(self, futureX, futureY):       
            # Verificar si la posición (x, y) es transitable en la capa Wall.
            tile_x = int(futureX / self.tile_width)
            tile_y = int(futureY / self.tile_height)

            if len(self.wall_layer.data) > tile_y >= 0 and len(self.wall_layer.data[0]) > tile_x >= 0:
                ID_tile = self.wall_layer.data[tile_y][tile_x]
                if ID_tile == FREE_TILE:
                    # logica SOLO para bloques con colisionadores de pygame
                    future_player_position = pygame.Rect(futureX * self.game_scale, futureY * self.game_scale,
                                            self.player.size * self.game_scale, self.player.size * self.game_scale)

                    for block in self.blocks:
                        if future_player_position.colliderect(block.collision_block):
                            # Hay una colisión con un bloque, no permitir el movimiento
                            return False
                    # No hay colisión con bloques, permitir el movimiento
                    return True
            return False

    def run(self):
        # Bucle principal
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            
            # Mover al jugador una baldosa cuando se presiona una tecla y la posición es transitable 
            if keys[pygame.K_UP] and self.can_move_to(self.player.posX, self.player.posY - self.player.speed):
                self.player.move(0, -PLAYER_SPEED)
            elif keys[pygame.K_DOWN] and self.can_move_to(self.player.posX, self.player.posY + self.player.speed):
                self.player.move(0, PLAYER_SPEED)
            elif keys[pygame.K_LEFT] and self.can_move_to(self.player.posX - self.player.speed, self.player.posY):
                self.player.move(-PLAYER_SPEED, 0)
            elif keys[pygame.K_RIGHT] and self.can_move_to(self.player.posX + self.player.speed, self.player.posY):
                self.player.move(PLAYER_SPEED, 0)
            if keys[pygame.K_SPACE]:
                # Coloca la bomba en la posición del jugador ajustada a la cuadrícula
                bomb_x =  self.player.posX
                bomb_y =  self.player.posY
                bomb = Bomb(bomb_x, bomb_y, PLAYER_SIZE, BLOCK_BOMB, GAME_SCALE,10)
                self.bombs.append(bomb)
            #controlar las bombas que ya explotaron y las que no
            bombsexploted=[]    
            for bomb in self.bombs:
                if bomb.exploded != False:
                    bombsexploted.append(bomb)

            self.bombs=bombsexploted

            #renderizado / etapa de dibujo en pantala
            # Limpiar la pantalla
            self.screen.fill(WHITE)

            # Dibujar el terreno y las paredes
            for layer in [self.terrain_layer, self.wall_layer]:
                for y, row in enumerate(layer.data):
                    for x, ID_tile in enumerate(row):
                        if ID_tile != NONE_TILE:
                            tile = self.tmx_map.get_tile_image_by_gid(ID_tile)
                            scaled_tile = pygame.transform.scale(tile, (int(self.tile_width * self.game_scale),
                                                                         int(self.tile_height * self.game_scale)))
                            self.screen.blit(scaled_tile, (x * self.tile_width * self.game_scale,
                                                           y * self.tile_height * self.game_scale))

                    
            # Dibujar al jugador
            for bomb in self.bombs[:]:
                bomb.update()
                bomb.draw(self.screen, self.game_scale)
            self.player.draw(self.screen, self.game_scale)

            # Dibujar bloques
            for block in self.blocks:
                block.draw(self.screen, self.game_scale)

            



            # Actualizar la pantalla
            pygame.display.flip()

            #pygame.time.delay(200)  # Añadimos un pequeño retraso para controlar la velocidad del jugador
            clock.tick(10)  # Controlar la velocidad del bucle principal / FPS por segundo

        pygame.quit()

        
game_engine = GameEngine(WIDTH_SCREEN , HEIGHT_SCREEN, GAME_SCALE, PLAYER_SIZE, PLAYER_SPEED)
game_engine.run()





xtemp = 10





xtemp = "hola mundo"




funcionX(xtemp)