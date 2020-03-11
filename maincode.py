import pygame
import os


def end_screen():
    pass


def main_code():
    board = Board.load('project/data/level_maps/level_beta.txt')
    player = board.get_player()
    running = True
    board.render(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                button = event.key
                if button in Object.DIFF:
                    player.move(button, board)
                    if not board.any_boxes():
                        end_screen()
            screen.fill((0, 0, 0))
            board.render(screen)
            pygame.display.flip()


def start_screen():
    intro_text = ["Сокобан", "",
                  "Нажмите где угодно",
                  "чтобы начать"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (500, 500))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return main_code()
        pygame.display.flip()


def load_image(name):
    fullname = os.path.join('project/data/sprites', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


class Object(pygame.sprite.Sprite):
    DIFF = {
        pygame.K_UP: (0, -1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0),
        pygame.K_DOWN: (0, 1),
    }

    def __init__(self, grp, coords):
        super().__init__(grp)
        self.coords = coords

    def move(self, dir, brd):
        return False

    def move_sprite(self):
        self.rect.x, self.rect.y = self.coords[0] * 50, self.coords[1] * 50


class Player(Object):
    SYMBOL = 'H'

    def __init__(self, group, coords):
        super().__init__(group, coords)
        self.group = group
        self.image = pygame.transform.scale(load_image('chelovechek.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.move_sprite()
        self.coords = coords

    def move(self, dir, brd):
        x, y = self.coords
        x, y = x + self.DIFF[dir][0], y + self.DIFF[dir][1]
        ob = brd.get_object((x, y))
        if ob.move(dir, brd):
            brd.objects.pop(self.coords)
            self.coords = (x, y)
            brd.objects[self.coords] = self
            self.move_sprite()


class Wall(Object):
    SYMBOL = '#'

    def __init__(self, group, coords):
        super().__init__(group, coords)
        self.image = load_image('wall.png')
        self.rect = self.image.get_rect()
        self.move_sprite()
        self.image = pygame.transform.scale(self.image, (50, 50))


class Grass(Object):
    SYMBOL = '.'

    def __init__(self, group, coords):
        super().__init__(group, coords)
        self.image = load_image('grass.png')
        self.rect = self.image.get_rect()
        self.move_sprite()

    def move(self, dir, brd):
        return True


class Box(Object):
    SYMBOL = '%'

    def __init__(self, group, coords):
        super().__init__(group, coords)
        self.image = load_image('box.png')
        self.rect = self.image.get_rect()
        self.move_sprite()

    def move(self, dir, brd):
        x, y = self.coords
        x, y = x + self.DIFF[dir][0], y + self.DIFF[dir][1]
        ob = brd.get_object((x, y))
        if isinstance(ob, Place):
            brd.objects.pop(self.coords)
            brd.object_sprites.remove(self)
            brd.cells[y][x] = Grass(brd.ground_sprites, (x, y))
            brd.ground_sprites.remove(ob)
            return True
        elif not isinstance(ob, Box) and ob.move(dir, brd):
            brd.objects.pop(self.coords)
            self.coords = (x, y)
            brd.objects[self.coords] = self
            self.move_sprite()
            return True
        return False


class Place(Grass):
    SYMBOL = '+'

    def __init__(self, group, coords):
        super().__init__(group, coords)
        self.image = load_image('fall.png')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.move_sprite()


class Board:
    def __init__(self, cells):
        self.ground_sprites = pygame.sprite.Group()
        self.object_sprites = pygame.sprite.Group()
        class_type = {
            '#': Wall,
            '.': Grass,
            '%': Grass,
            '+': Place,
            'H': Grass,
        }
        self.cells = [
            [
                class_type[q](self.ground_sprites, (x, y))
                for x, q in enumerate(a)
            ]
            for y, a in enumerate(cells)
        ]
        class_type = {
            'H': Player,
            '%': Box,
        }
        self.objects = {
            (x, y): class_type[q](self.object_sprites, (x, y))
            for y, a in enumerate(cells)
            for x, q in enumerate(a)
            if q in class_type
        }
        self.height = 7
        self.width = 10
        self.coords = list()
        self.color = (255, 255, 255)
        self.left = 0
        self.top = 0
        self.cell_size = 50
        self.wholelist = {}
        self.startplayercoords = 0, 0

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf8") as level_prot:
            lines = level_prot.readlines()
            lines = [a.strip() for a in lines]
            lines = [a for a in lines if a]
            return cls(lines)

    def render(self, place):
        self.ground_sprites.draw(place)
        self.object_sprites.draw(place)

    def get_object(self, crds):
        x, y = crds
        if (x, y) in self.objects:
            return self.objects[(x, y)]
        return self.cells[y][x]

    def get_player(self):
        for i in self.objects.values():
            if isinstance(i, Player):
                return i

    def any_boxes(self):
        for i in self.objects.values():
            if isinstance(i, Box):
                return True
        return False


pygame.init()
screen = pygame.display.set_mode((500, 350), flags=pygame.SRCALPHA)
start_screen()