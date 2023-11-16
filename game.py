import pygame
import pytmx

# variables globales
WIDTH_SCREEN, HEIGHT_SCREEN = 272, 208
PLAYER_SIZE = 16
TILE_SIZE = 16
POSITION_PLAYER_X, POSITION_PLAYER_Y = 2, 1
GAME_SCALE = 3
FREE_TILE = 0
NONE_TILE = 0
PLAYER_SPEED = PLAYER_SIZE
WHITE = (0, 0, 0)
PATH_STAGE1_MAP = "TiledMap/Stage1/Stage1.tmx"
PATH_PLAYER_SPRITE= "Sprites/bomberman_main.png"
PATH_BLOCK_SPRITE= "Sprites/block_town.png"
PATH_BOMB_SPRITE= "Sprites/bomb.png"
PATH_EXPLOTION_SPRITE= "Sprites/explotion.png"
PATH_TILE_SPRITE= "Sprites/stage1_tile.png"
EXPLOSION_RADIUS = 1
EXPLOSION_TIME = 18
CLOCK_TIME = 8

class Player:
    def __init__(self, x, y, size, speed, sprite, game_scale, tile_size):
        self.posX = x * tile_size
        self.posY = y * tile_size
        self.size = size
        self.speed = speed
        self.scaled_player_sprite = self.load_sprites(sprite, game_scale, size)

    def load_sprites(self, sprite_name, game_scale, size):
        sprite = pygame.image.load(sprite_name)
        # Escala la imagen al tamaño del jugador
        scaled_player_sprite = pygame.transform.scale(sprite, (game_scale * size, size * game_scale))
        return scaled_player_sprite

    def move(self, movement_x, movement_y):
        self.posX += movement_x     #offset_x
        self.posY += movement_y 

    def draw(self, game_window, scale_game):
        scaled_size = int(self.size * scale_game)
        scaled_player_rect = pygame.Rect(self.posX * scale_game, self.posY * scale_game, scaled_size, scaled_size)
        # Dibuja el sprite en pantalla
        game_window.blit(self.scaled_player_sprite, scaled_player_rect)


class Destructible_Tile:
    collision_block = None
    def __init__(self, x, y, size, sprite, game_scale, tile_size):
        self.posX = x * tile_size
        self.posY = y * tile_size
        self.size = size
        self.animation_destructible_tile = Animation(sprite, 4, CLOCK_TIME, game_scale)

    def draw(self, game_window, scale_game):
        scaled_size = int(self.size * scale_game)
        game_window.blit(self.animation_destructible_tile.get_current_frame(), (self.posX * scale_game, self.posY * scale_game))
        self.collision_block  = pygame.Rect(self.posX * scale_game, self.posY * scale_game, scaled_size, scaled_size)


                
class Bomb:
    def __init__(self, x, y, size, sprite_bomb, sprite_explotion, game_scale, explosion_radius, explosion_time, game_map):
        self.posX = x
        self.posY = y
        self.size = size
        self.game_scale = game_scale
        self.explotion_radius = explosion_radius
        self.explotion_time = explosion_time
        self.exploded = False
        self.destroy_tiles_in_radius(game_map, self.posX, self.posY, explosion_radius)
    
        #animacion
        self.animation_Bomb = Animation(sprite_bomb, 3, CLOCK_TIME, game_scale)
        self.animation_Explotion = Animation(sprite_explotion, 2, CLOCK_TIME, game_scale)


    def draw(self, game_window, scale_game):
        game_window.blit(self.animation_Bomb.get_current_frame(), (self.posX * scale_game, self.posY * scale_game))


    def explotion_countdown(self, game_window):
        if not self.exploded:
            self.explotion_time -= 1
            if self.explotion_time <= 0:
                self.exploded = True
                game_window.blit(self.animation_Explotion.get_current_frame(), ((self.posX-32) * self.game_scale, (self.posY-32) * self.game_scale))

    def destroy_tiles_in_radius(self, map_wall, bomb_posX, bomb_posY, explosion_radius):
        bomb_posX = int(bomb_posX/self.size)
        bomb_posY = int(bomb_posY/self.size)
        # Destruir en la fila horizontal hacia la izquierda
        for offset_x in range(1, explosion_radius + 1):
            tile_x = bomb_posX - offset_x
            if 0 <= tile_x < len(map_wall[0]):
                if map_wall[bomb_posY][tile_x] == NONE_TILE:
                    print("anima <-")
                    print(map_wall[bomb_posY][tile_x])
                else:
                    break
        # Destruir en la fila horizontal hacia la derecha
        for offset_x in range(1, explosion_radius + 1):
            #tile_x = int(bomb_posX/self.size) + offset_x
            tile_x = bomb_posX + offset_x
            if 0 <= tile_x < len(map_wall[0]):
                if map_wall[bomb_posY][tile_x] == NONE_TILE:
                    print("anima ->")
                    print(map_wall[bomb_posY][tile_x])
                else:
                    break
               
        # Destruir en la columna vertical hacia arriba
        for offset_y in range(1, explosion_radius + 1):
            tile_y = bomb_posY - offset_y
            if 0 <= tile_y < len(map_wall):
                if map_wall[tile_y][bomb_posX] == NONE_TILE:
                    print("anima up") 
                    print(map_wall[tile_y][bomb_posX])
                else:
                    break
                    
        # Destruir en la columna vertical hacia abajo
        for offset_y in range(1, explosion_radius+1):
            tile_y = bomb_posY + offset_y
            if 0 <= tile_y < len(map_wall):
                if map_wall[tile_y][bomb_posX] == NONE_TILE:
                    print("anima down")
                    print(map_wall[tile_y][bomb_posX])
                else:
                    break
                         
    def check_for_enemy_hits(self):
        print("en progreso")

    def check_for_bomberman_hit(self):
        print("en progreso")

class Animation:
    def __init__(self, sprite_name, num_frames, speed, game_scale):
        self.animation_speed = speed
        self.frame_index = 0
        self.num_frames = num_frames
        self.frames = self.load_sprites(sprite_name, num_frames, game_scale)
        self.game_scale = game_scale

    def load_sprites(self, sprite_name, num_frames, game_scale):
        sprite_sheet = pygame.image.load(sprite_name)
        sprite_sheet = pygame.transform.scale(sprite_sheet, (game_scale* sprite_sheet.get_width(), sprite_sheet.get_height() * game_scale))
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()
        #sprite_list = [sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(num_frames)]
        sprite_list = []
        for i in range(num_frames):
            frame_rect = pygame.Rect(i * frame_width , 0, frame_width, frame_height)
            frame_image = sprite_sheet.subsurface(frame_rect)
            sprite_list.append(frame_image)
        return sprite_list

    def get_current_frame(self):
        self.frame_index = (self.frame_index + 1) % self.num_frames
        return self.frames[self.frame_index]
    


class GameEngine:
    map_game = None
    def __init__(self, width, height, GAME_SCALE, player_size, player_speed):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((width * GAME_SCALE, height * GAME_SCALE))
        # Obtener las capas del mapa
        self.tmx_map = pytmx.load_pygame(PATH_STAGE1_MAP)
        self.terrain_layer = self.tmx_map.get_layer_by_name("Terrain")
        self.wall_layer = self.tmx_map.get_layer_by_name("Wall")
        self.block_layer = self.tmx_map.get_layer_by_name("Block")
        self.tile_width = self.tmx_map.tilewidth   
        self.tile_height = self.tmx_map.tileheight

        #instancias de objetos 
        self.player = Player(POSITION_PLAYER_X, POSITION_PLAYER_Y, player_size, player_speed, PATH_PLAYER_SPRITE, GAME_SCALE, self.tile_width)
        self.game_scale = GAME_SCALE
        # Lista para almacenar instancias de destructible_tile
        self.destructible_tile = []
        self.append_destructible_tile_matrix(self.block_layer)
        self.bombs = []

        self.merge_matrix(self.wall_layer.data, self.block_layer.data)

    def append_destructible_tile_matrix(self, layer):
        for row in range(len(layer.data)):
            for Column in range(len(layer.data[row])):
                ID_tile = layer.data[row][Column]
                if ID_tile != NONE_TILE:
                    block_size = self.tile_width  # Ajusta el tamaño según tus necesidades
                    block_sprite_path = PATH_TILE_SPRITE
                    block = Destructible_Tile(Column, row, block_size, block_sprite_path, self.game_scale, self.tile_width)
                    self.destructible_tile.append(block)


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

                for block in self.destructible_tile:
                    if future_player_position.colliderect(block.collision_block):
                        # Hay una colisión con un bloque, no permitir el movimiento
                        return False
                # No hay colisión con bloques, permitir el movimiento
                return True
        return False

    def merge_matrix(self, matrix_wall, matrix_block):
        rows = len(matrix_wall)
        cols = len(matrix_wall[0])

        # Inicializar map_game con los valores de la primera matriz
        self.map_game = [row.copy() for row in matrix_wall]
        # Actualizar map_game con los valores no nulos de la segunda matriz
        for i in range(rows):
            for j in range(cols):
                if matrix_block[i][j] != NONE_TILE:
                    self.map_game[i][j] = matrix_block[i][j]
        return self.map_game

    def draw_layer(self, layer):
        for row in range(len(layer.data)):
            for Column in range(len(layer.data[row])):
                ID_tile = layer.data[row][Column]
                if ID_tile != NONE_TILE:
                    tile = self.tmx_map.get_tile_image_by_gid(ID_tile)
                    scaled_tile = pygame.transform.scale(tile, (int(self.tile_width * self.game_scale),
                                                                int(self.tile_height * self.game_scale)))
                    self.screen.blit(scaled_tile, (Column  * self.tile_width * self.game_scale,
                                                row * self.tile_height * self.game_scale))


    def handle_inputs(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Detectar si la tecla de espacio está presionada
        if keys[pygame.K_SPACE]:
            Bomba = Bomb(self.player.posX, self.player.posY, self.player.size, PATH_BOMB_SPRITE, PATH_EXPLOTION_SPRITE, self.game_scale, EXPLOSION_RADIUS, EXPLOSION_TIME, self.map_game)   
            self.bombs.append(Bomba)
                
        # Mover al jugador una baldosa cuando se presiona una tecla y la posición es transitable 
        if keys[pygame.K_UP] and self.can_move_to(self.player.posX, self.player.posY - self.player.speed):
            self.player.move(0, -PLAYER_SPEED)
        elif keys[pygame.K_DOWN] and self.can_move_to(self.player.posX, self.player.posY + self.player.speed):
            self.player.move(0, PLAYER_SPEED)
        elif keys[pygame.K_LEFT] and self.can_move_to(self.player.posX - self.player.speed, self.player.posY):
            self.player.move(-PLAYER_SPEED, 0)
        elif keys[pygame.K_RIGHT] and self.can_move_to(self.player.posX + self.player.speed, self.player.posY):
            self.player.move(PLAYER_SPEED, 0)

    def update(self, clock):
        active_bombs = []  # Creamos una nueva lista para almacenar las bombas activas
        for bomb in self.bombs:
            if bomb.explotion_time > 0:
                active_bombs.append(bomb)
        self.bombs = active_bombs
    
        pygame.display.flip() # Actualizar la pantalla

        #pygame.time.delay(200)  # Añadimos un pequeño retraso para controlar la velocidad del jugador
        clock.tick(CLOCK_TIME)  # Controlar la velocidad del bucle principal / FPS por segundo

    def draw(self):
        self.screen.fill(WHITE) # Limpiar la pantalla       
            

        self.draw_layer(self.terrain_layer)

        for bomb in self.bombs:
            bomb.explotion_countdown(self.screen)

        self.draw_layer(self.wall_layer)

        # Dibujar bomba
        for bomb in self.bombs:
            bomb.draw(self.screen, self.game_scale)

        # Dibujar al jugador
        self.player.draw(self.screen, self.game_scale)

        # Dibujar bloques
        for block in self.destructible_tile:
            block.draw(self.screen, self.game_scale)


        

    def run(self):
        clock = pygame.time.Clock()
        while self.running: # Bucle principal
            self.handle_inputs()
            self.draw()
            self.update(clock)
        pygame.quit()

  
game_engine = GameEngine(WIDTH_SCREEN , HEIGHT_SCREEN, GAME_SCALE, PLAYER_SIZE, PLAYER_SPEED)
game_engine.run()




