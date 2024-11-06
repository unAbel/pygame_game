import pygame
import pytmx

# global variables
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
PATH_BOMB_SPRITE= "Sprites/bomb1.png"
PATH_EXPLOTION_SPRITE= "Sprites/explotion.png"
PATH_TILE_SPRITE= "Sprites/block_town.png"
EXPLOSION_RADIUS = 3
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
        # Scale the image 16*16 pixel
        scaled_player_sprite = pygame.transform.scale(sprite, (game_scale * size, size * game_scale))
        return scaled_player_sprite

    def move(self, movement_x, movement_y):
        self.posX += movement_x     #offset_x
        self.posY += movement_y 

    def draw(self, game_window, scale_game):
        scaled_size = int(self.size * scale_game)
        scaled_player_rect = pygame.Rect(self.posX * scale_game, self.posY * scale_game, scaled_size, scaled_size)
        # Draw the sprite on the game window
        game_window.blit(self.scaled_player_sprite, scaled_player_rect)


class Destructible_Tile:
    collision_tile = None
    def __init__(self, x, y, size, sprite, game_scale, tile_size):
        self.posX = x * tile_size
        self.posY = y * tile_size
        self.size = size
        self.scaled_destructible_tile = self.load_sprites(sprite, game_scale, size)

    def load_sprites(self, sprite_name, game_scale, size):
        sprite = pygame.image.load(sprite_name)
        destructible_tile = pygame.transform.scale(sprite, (game_scale * size, size * game_scale))
        return destructible_tile
    
    def draw(self, game_window, scale_game):
        scaled_size = int(self.size * scale_game)
        scaled_tile_rect = pygame.Rect(self.posX * scale_game, self.posY * scale_game, scaled_size, scaled_size)
        game_window.blit(self.scaled_destructible_tile, scaled_tile_rect)
        # collision var
        self.collision_tile = scaled_tile_rect

                
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
        self.sprite_Bomb = self.load_sprites(sprite_bomb, game_scale, size)

    def load_sprites(self, sprite_name, game_scale, size):
        sprite = pygame.image.load(sprite_name)
        sprite_bomb = pygame.transform.scale(sprite, (game_scale * size, size * game_scale))
        return sprite_bomb
    
    def draw(self, game_window, scale_game):
        scaled_size = int(self.size * scale_game)
        scaled_bomb_rect = pygame.Rect(self.posX * scale_game, self.posY * scale_game, scaled_size, scaled_size)
        game_window.blit(self.sprite_Bomb, scaled_bomb_rect)

    def explotion_countdown(self, game_window):
        if not self.exploded:
            self.explotion_time -= 1
            if self.explotion_time <= 0:
                self.exploded = True
                #missing explosion sprite here

    def destroy_tiles_in_radius(self, map_wall, bomb_posX, bomb_posY, explosion_radius):
        print("BOOM!")
        bomb_posX = int(bomb_posX/self.size)
        bomb_posY = int(bomb_posY/self.size)
        # <- left in progress
        for offset_x in range(1, explosion_radius + 1):
            tile_x = bomb_posX - offset_x
            if 0 <= tile_x < len(map_wall[0]):
                if map_wall[bomb_posY][tile_x] == NONE_TILE:
                    print("<-")
                    print(map_wall[bomb_posY][tile_x])
                else:
                    break
        # -> right in progress
        for offset_x in range(1, explosion_radius + 1):
            tile_x = bomb_posX + offset_x
            if 0 <= tile_x < len(map_wall[0]):
                if map_wall[bomb_posY][tile_x] == NONE_TILE:
                    print("->")
                    print(map_wall[bomb_posY][tile_x])
                else:
                    break
               
        # up in progress
        for offset_y in range(1, explosion_radius + 1):
            tile_y = bomb_posY - offset_y
            if 0 <= tile_y < len(map_wall):
                if map_wall[tile_y][bomb_posX] == NONE_TILE:
                    print("up") 
                    print(map_wall[tile_y][bomb_posX])
                else:
                    break
                    
        # down in progress
        for offset_y in range(1, explosion_radius+1):
            tile_y = bomb_posY + offset_y
            if 0 <= tile_y < len(map_wall):
                if map_wall[tile_y][bomb_posX] == NONE_TILE:
                    print("down")
                    print(map_wall[tile_y][bomb_posX])
                else:
                    break
                         
    def check_for_enemy_hits(self):
        print("in progress")

    def check_for_bomberman_hit(self):
        print("in progress")


class GameEngine:
    map_game = None
    def __init__(self, width, height, GAME_SCALE, player_size, player_speed):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((width * GAME_SCALE, height * GAME_SCALE))
        # get layers from TILED
        self.tmx_map = pytmx.load_pygame(PATH_STAGE1_MAP)
        self.terrain_layer = self.tmx_map.get_layer_by_name("Terrain")
        self.wall_layer = self.tmx_map.get_layer_by_name("Wall")
        self.block_layer = self.tmx_map.get_layer_by_name("Block")
        self.tile_width = self.tmx_map.tilewidth   
        self.tile_height = self.tmx_map.tileheight

        #objects (player, tile, bomb...) 
        self.player = Player(POSITION_PLAYER_X, POSITION_PLAYER_Y, player_size, player_speed, PATH_PLAYER_SPRITE, GAME_SCALE, self.tile_width)
        self.game_scale = GAME_SCALE
        self.destructible_tile = []
        self.append_destructible_tile_matrix(self.block_layer)
        self.bombs = []
        self.merge_matrix(self.wall_layer.data, self.block_layer.data)

    def append_destructible_tile_matrix(self, layer):
        for row in range(len(layer.data)):
            for Column in range(len(layer.data[row])):
                ID_tile = layer.data[row][Column]
                if ID_tile != NONE_TILE:
                    block_size = self.tile_width  
                    block_sprite_path = PATH_TILE_SPRITE
                    block = Destructible_Tile(Column, row, block_size, block_sprite_path, self.game_scale, self.tile_width)
                    self.destructible_tile.append(block)


    def can_move_to(self, futureX, futureY):       
        tile_x = int(futureX / self.tile_width)
        tile_y = int(futureY / self.tile_height)
        if len(self.wall_layer.data) > tile_y >= 0 and len(self.wall_layer.data[0]) > tile_x >= 0:
            ID_tile = self.wall_layer.data[tile_y][tile_x]
            if ID_tile == FREE_TILE: # check if can be moved (wall_layer)
                # check if can be moved (block_layer)
                future_player_position = pygame.Rect(futureX * self.game_scale, futureY * self.game_scale,
                                            self.player.size * self.game_scale, self.player.size * self.game_scale)
                for block in self.destructible_tile:
                    if future_player_position.colliderect(block.collision_tile):
                        return False
                return True
        return False

    def merge_matrix(self, matrix_wall, matrix_block): # merge wall_layer and block_layer in map_game
        rows = len(matrix_wall)
        cols = len(matrix_wall[0])
        self.map_game = [row.copy() for row in matrix_wall]
        for i in range(rows):
            for j in range(cols):
                if matrix_block[i][j] != NONE_TILE:
                    self.map_game[i][j] = matrix_block[i][j]
        return self.map_game    # matrix for game map

    def draw_layer(self, layer): # draw wall_layer and terrain_layer
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

        # SPACE
        if keys[pygame.K_SPACE]:
            Bomba = Bomb(self.player.posX, self.player.posY, self.player.size, PATH_BOMB_SPRITE, PATH_EXPLOTION_SPRITE, self.game_scale, EXPLOSION_RADIUS, EXPLOSION_TIME, self.map_game)   
            self.bombs.append(Bomba)
                
        # 
        if keys[pygame.K_UP] and self.can_move_to(self.player.posX, self.player.posY - self.player.speed):
            self.player.move(0, -PLAYER_SPEED)
        elif keys[pygame.K_DOWN] and self.can_move_to(self.player.posX, self.player.posY + self.player.speed):
            self.player.move(0, PLAYER_SPEED)
        elif keys[pygame.K_LEFT] and self.can_move_to(self.player.posX - self.player.speed, self.player.posY):
            self.player.move(-PLAYER_SPEED, 0)
        elif keys[pygame.K_RIGHT] and self.can_move_to(self.player.posX + self.player.speed, self.player.posY):
            self.player.move(PLAYER_SPEED, 0)

    def update(self, clock):
        active_bombs = []  # update bombs in game
        for bomb in self.bombs:
            if bomb.explotion_time > 0:
                active_bombs.append(bomb)
        self.bombs = active_bombs
    
        for bomb in self.bombs: #update bomb timer
            bomb.explotion_countdown(self.screen)

        pygame.display.flip() # update screen
        clock.tick(CLOCK_TIME)  # speed of main loop / FPS 

    def draw(self):
        self.screen.fill(WHITE) # Limpiar la pantalla       
            
        self.draw_layer(self.terrain_layer)

        self.draw_layer(self.wall_layer)

        for bomb in self.bombs:
            bomb.draw(self.screen, self.game_scale, )

        for block in self.destructible_tile:
            block.draw(self.screen, self.game_scale)

        self.player.draw(self.screen, self.game_scale)
        

    def run(self):
        clock = pygame.time.Clock()
        while self.running: # main loop
            self.handle_inputs()
            self.draw()
            self.update(clock)
        pygame.quit()

game_engine = GameEngine(WIDTH_SCREEN , HEIGHT_SCREEN, GAME_SCALE, PLAYER_SIZE, PLAYER_SPEED)
game_engine.run()

