import pygame


class Board:
    def __init__(self, width, height, targlst):
        self.width = width
        self.height = height
        self.coords = list()
        self.color = (255, 255, 255)
        self.left = 10
        self.top = 10
        self.cell_size = 30
        targ = targlst
        for i in range(self.width):
            self.coords.append(list())
            for q in range(self.height):
                self.coords[i].append([(i + self.left) * self.cell_size, (q + self.top) * self.cell_size, self.color, targ])

    def render(self, place):
        for q in range(self.height):
            for y in range(self.width):
                pygame.draw.rect(place, (255, 255, 255),
                                 pygame.Rect(self.left + y * self.cell_size, self.top + q * self.cell_size,
                                             self.cell_size, self.cell_size), 1)

    def coord_print(self, crds):
        if crds[1] <= self.height * self.cell_size + self.top:
            if crds[0] <= self.width * self.cell_size + self.left:
                x = (crds[0] - self.left) // self.cell_size
                y = (crds[1] - self.top) // self.cell_size
                return (x, y)
            else:
                return None
        else:
            return None

    def check_fill(self, crd):
        a = self.coord_print(crd)
        if a:
            for q in range(self.height):
                for y in range(self.width):
                    if a[0] == self.coords[q][y][0] // self.cell_size + self.left:
                        if a[1] == self.coords[q][y][1] // self.cell_size + self.top:
                            return


class Player(pygame.sprite.Sprite):
    image = load_image("chelovechek.png")

    def __init__(self, group, crd, brd):
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = crd[0]
        self.rect.y = crd[1]
        self.board = brd

    def check(self, dir):
        if dir == 'up':
            if brd.check_fill(self.rect.y - 30)

    def move(self, event):
        if event == pygame.KEYUP:
            if check('up')



pygame.init()
screen = pygame.display.set_mode((500, 500))
get_lst = list()
board = Board(10, 10, get_lst)
running = True
board.set_view(20, 20, 40)
board.render(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.coord_print(event.pos)
        pygame.display.flip()