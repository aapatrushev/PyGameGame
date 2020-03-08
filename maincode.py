import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('project/data/sprites', name)
    image = pygame.image.load(fullname).convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, group, coords):
        super().__init__(group)
        self.group = group
        self.image = pygame.transform.scale(load_image('chelovechek.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def move(self, dir):
        if dir == 'up':
            self.rect.y -= 50
        if dir == 'down':
            self.rect.y += 50
        if dir == 'right':
            self.rect.x += 50
        if dir == 'left':
            self.rect.x -= 50
        print(board.get_type((self.rect.x, self.rect.y)))


class Box(pygame.sprite.Sprite):
    def __init__(self, group, coords):
        super().__init__(group)
        self.image = load_image('box.png')
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def move(self, dir, brd):
        if dir == 'up':
            self.rect.y -= 50
            for i in range(len(brd.coords)):
                for q in range(len(brd.coords[i])):
                    if brd.coords[i][q][0] == self.rect.y and brd.coords[i][q][1] == self.rect.x:
                        brd.coords[i][q][2] = '.'
                        brd.coords[i - 1][q][2] = '%'
        if dir == 'down':
            self.rect.y += 50
        if dir == 'right':
            self.rect.x += 50
        if dir == 'left':
            self.rect.x -= 50


class Board:
    def __init__(self, targlst, grp):
        self.height = 7
        self.width = 10
        self.coords = list()
        self.color = (255, 255, 255)
        self.left = 0
        self.top = 0
        self.cell_size = 50
        self.sprites = grp
        self.boxlist = []
        self.startplayercoords = 0, 0
        for i in range(self.height):
            self.coords.append(list())
            for q in range(self.width):
                targ = targlst[i + 1][q]
                self.coords[i].append([i * self.cell_size, q * self.cell_size, targ])
                sprite = pygame.sprite.Sprite(self.sprites)
                if targ == '%':
                    sprite.image = load_image('grass.png')
                    self.boxlist.append(Box(self.sprites, (q * self.cell_size, i * self.cell_size)))
                elif targ == '#':
                    sprite.image = load_image('wall.png')
                elif targ == '+':
                    sprite.image = load_image('creature.png')
                elif targ == 'H':
                    sprite.image = load_image('grass.png')
                    self.startplayercoords = q * self.cell_size, i * self.cell_size
                else:
                    sprite.image = load_image('grass.png')
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = q * self.cell_size
                sprite.rect.y = i * self.cell_size
                sprite.image = pygame.transform.scale(sprite.image, (50, 50))

    def render(self, place):
        self.sprites.draw(place)

    def get_type(self, crds):
        return self.coords[crds[1] // self.cell_size][crds[0] // self.cell_size][2]

    def get_list_part(self, crds):
        return crds[1] // self.cell_size, crds[0] // self.cell_size


get_lst = list()
m = 0
with open('project/data/level_maps/level_beta.txt', encoding="utf8") as level_prot:
    lst = level_prot.readlines()
    for a in range(len(lst)):
        get_lst.append(lst[a])
        for q in range(len(lst[a])):
            if lst[a][q] == '+':
                m += 1
win_as = [0, m]
pygame.init()
screen = pygame.display.set_mode((500, 350))
all_sprites = pygame.sprite.Group()
board = Board(get_lst, all_sprites)
player = Player(all_sprites, board.startplayercoords)
running = True
board.render(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # if board.get_type((player.rect.x, player.rect.y + 50)) == '%':
            #     if board.get_type((player.rect.x, player.rect.y + 100)) != '#':
            #         pt = board.get_list_part((player.rect.x, player.rect.y + 50))
            #         board.coords[pt[0]][pt[1]][2], board.coords[pt[0] + 1][pt[1]][2] = \
            #             board.coords[pt[0] + 1][pt[1]][2], board.coords[pt[0]][pt[1]][2]
            #         player.move('down')
            # elif board.get_type((player.rect.x, player.rect.y + 50)) != '#':
            #     player.move('down')
            button = event.key
            diff = {
                pygame.K_UP: (0, -50, 'up'),
                pygame.K_LEFT: (-50, 0, 'left'),
                pygame.K_RIGHT: (50, 0, 'right'),
                pygame.K_DOWN: (0, 50, 'down'),
            }
            if button in diff:
                diff = diff[button]
                if board.get_type((player.rect.x + diff[0], player.rect.y + diff[1])) != '#':
                    player.move(diff[2])
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()