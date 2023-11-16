import pygame
import pytmx



# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)

# Configuración de la pantalla
WIDTH, HEIGHT = 272, 208
TILE_SIZE = 3
screen = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE))
pygame.display.set_caption("Juego con Tiled Map")

# Cargar el mapa creado con Tiled
tmx_map = pytmx.load_pygame("TiledMap/Stage1/Stage1.tmx")

# Obtener las capas del mapa
terrain_layer = tmx_map.get_layer_by_name("Terrain")
wall_layer = tmx_map.get_layer_by_name("Wall")

# Tamaño de los tiles
tile_width = tmx_map.tilewidth
tile_height = tmx_map.tileheight

# Tamaño del jugador (ajustado al tamaño de una baldosa)
player_size = tile_width
player_x = 32
player_y = 32
player_speed = tile_width

# Factor de escala para los sprites del Tiled
sprite_scale = TILE_SIZE  # Puedes ajustar esto según tus necesidades

def can_move_to(x, y):
    #Verificar si la posición (x, y) es transitable en la capa Wall.
    tile_x = int(x / tile_width)
    tile_y = int(y / tile_height)

    if 0 <= tile_y < len(wall_layer.data) and 0 <= tile_x < len(wall_layer.data[0]):
        gid = wall_layer.data[tile_y][tile_x]
        return gid == 0

    return False

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Mover al jugador una baldosa cuando se presiona una tecla y la posición es transitable
    if keys[pygame.K_UP] and can_move_to(player_x, player_y - player_speed):
        player_y -= player_speed
    elif keys[pygame.K_DOWN] and can_move_to(player_x, player_y + player_speed):
        player_y += player_speed
    elif keys[pygame.K_LEFT] and can_move_to(player_x - player_speed, player_y):
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and can_move_to(player_x + player_speed, player_y):
        player_x += player_speed

    # Limpiar la pantalla
    screen.fill((0, 0, 0))

    # Dibujar el terreno y las paredes
    for layer in [terrain_layer, wall_layer]:
        for y, row in enumerate(layer.data):
            for x, gid in enumerate(row):
                if gid:
                    tile = tmx_map.get_tile_image_by_gid(gid)
                    scaled_tile = pygame.transform.scale(tile, (int(tile_width * sprite_scale), int(tile_height * sprite_scale)))
                    screen.blit(scaled_tile, (x * tile_width * sprite_scale, y * tile_height * sprite_scale))

    # Dibujar al jugador con el factor de escala
    pygame.draw.rect(screen, WHITE, (player_x * sprite_scale, player_y * sprite_scale, player_size * sprite_scale, player_size * sprite_scale))

    pygame.display.flip()

    pygame.time.delay(100)  # Añadimos un pequeño retraso para controlar la velocidad del jugador

pygame.quit()