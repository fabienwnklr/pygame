import pygame
import pytmx
import pyscroll

from player import Player


class Game:
    def __init__(self):
        # créer la fenêtre
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Pygame - Houwou')

        # charger la carte (.tmx)
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.BufferedRenderer(
            map_data, self.screen.get_size())

        # générer un joueur
        player_position = tmx_data.get_object_by_name('player')
        self.player = Player(player_position.x, player_position.y)

        # liste des collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(
                    obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(
            map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.change_animation('up')
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.change_animation('down')
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.change_animation('left')
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.change_animation('right')
            self.player.move_right()

    def update(self):
        self.group.update()

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()

        # boucle du jeu
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()
