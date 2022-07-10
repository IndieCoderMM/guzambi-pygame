from .constants import WIDTH, HEIGHT, MARGIN, TILE_WIDTH, HEADER, LEGENDS, ITEMS, DICE, WHITE, RED, BLUE, BLACK, GREEN, BOARD_WIDTH, BGIMG, FOOTER, BLANK_CARDS, CardType
from .player import Player
from .board import Board
import pygame

class GUI:
    def __init__(self, title: str):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)

    @staticmethod
    def get_left_top(col: int, row: int) -> tuple[int, int]:
        left = MARGIN + (col * TILE_WIDTH) + (col - 1)
        top = HEADER + (row * TILE_WIDTH) + (row - 1)
        return left, top

    @staticmethod
    def get_selected_hero(pos):
        x, y = pos
        for hero in LEGENDS:
            if hero.card_rect.collidepoint(x, y):
                return hero
        return None

    @staticmethod
    def dice_clicked(pos):
        x, y = pos
        if DICE.rect.collidepoint(x, y):
            return True
        return False

    def display_text(self, txt: str, color: tuple, size: int, x: int = 0, y: int = 0, align: str = 'None'):
        font = pygame.font.SysFont('comicsans', size)
        text = font.render(txt, True, color)
        if align == 'center':
            x = WIDTH // 2 - text.get_width() // 2
        elif align == 'right':
            x = WIDTH - text.get_width() - MARGIN
        elif align == 'left':
            x = MARGIN
        self.window.blit(text, (x, y))

    def draw_health_bar(self, player: Player, x: int, y: int, length: int, thickness: int = 20):
        pygame.draw.rect(self.window, RED, (x, y, length, thickness))
        bar_length = length * player.health // player.max_health
        if player.id == 'P2':
            x += length - bar_length

        pygame.draw.rect(self.window, GREEN, (x, y, bar_length, thickness))

    def display_status(self, p1: Player, p2: Player):
        self.display_text(p1.hero_name, WHITE, 25, y=10, align='left')
        self.display_text(p2.hero_name, WHITE, 25, y=10, align='right')
        bar_length = 150
        p1.add_item(ITEMS[0])
        p1.add_item(ITEMS[1])
        p2.add_item(ITEMS[2])
        self.draw_health_bar(p1, MARGIN, 50, bar_length)
        self.draw_health_bar(p2, WIDTH - MARGIN - bar_length, 50, bar_length)
        self.draw_items(p1)
        self.draw_items(p2)

    def draw_items(self, player: Player):
        for index, item in enumerate(player.inventory):
            if item.type == CardType.HEAL or item.type == CardType.SPEED:
                continue
            y = HEADER - item.icon.get_width() - 10
            if player.id == 'P1':
                x = MARGIN + (item.icon.get_width() + 10) * index
            else:
                x = WIDTH - MARGIN - item.icon.get_width() * (index+1) - 10 * index

            self.window.blit(item.icon, (x, y))

    def draw_tile(self, num: int, row: int, col: int):
        left, top = self.get_left_top(col, row)
        pygame.draw.rect(self.window, WHITE, (left, top, TILE_WIDTH, TILE_WIDTH), 1)
        textx = left + int(TILE_WIDTH / 2)
        texty = top + int(TILE_WIDTH / 2)
        self.display_text(str(num), RED, 20, textx, texty)

    def draw_board(self, board: Board):
        left, top = self.get_left_top(0, 0)
        pygame.draw.rect(self.window, GREEN, (left, top, BOARD_WIDTH, BOARD_WIDTH))
        self.window.blit(BGIMG, (left, top))
        for row in range(board.ROWS):
            for col in range(board.COLS):
                self.draw_tile(board.tile(row, col), row, col)
        pygame.draw.rect(self.window, BLACK, (left - 5, top - 5, BOARD_WIDTH + 12, BOARD_WIDTH + 12), 4)

    def draw_player(self, board: Board):
        for col in range(board.COLS):
            for row in range(board.ROWS):
                if board.tile(row, col) == board.p1.tile:
                    player_img = board.p1.sprite
                    x, y = self.get_left_top(col, row)
                    self.window.blit(player_img, (x, y))
                if board.tile(row, col) == board.p2.tile:
                    player_img = board.p2.sprite
                    x, y = self.get_left_top(col, row)
                    x += TILE_WIDTH // 2
                    y += TILE_WIDTH // 2
                    self.window.blit(player_img, (x, y))

    def draw_card(self, card_img, rect: tuple, bgcolor: tuple, pos: tuple[int, int]):
        rect.topleft = pos
        pygame.draw.rect(self.window, bgcolor, rect)
        self.window.blit(card_img, pos)

    def display_selection(self):
        for i, hero in enumerate(LEGENDS):
            y = HEIGHT - FOOTER - hero.card_rect.height
            gap = ((WIDTH - MARGIN * 2) - hero.card_rect.width * len(LEGENDS)) // (len(LEGENDS)+1)
            x = MARGIN + hero.card_rect.width * i + gap * (i+1)
            self.draw_card(hero.card, hero.card_rect, WHITE, (x, y))

    def display_menu(self):
        self.window.fill(BLUE)
        self.display_text('GUZAMBI:', WHITE, 50, 10, 10)
        self.display_text('Choose Your Character...', WHITE, 30, 30, 110)
        self.display_selection()
        pygame.display.update()

    def display_fortune_card(self, card):
        x = MARGIN + BOARD_WIDTH + 20
        y = HEADER + 20
        self.draw_card(card, card.get_rect(), WHITE, (x, y))

    def display_game(self, board: Board):
        self.window.fill(BLUE)
        self.draw_board(board)
        self.draw_player(board)
        self.display_status(board.p1, board.p2)
        self.display_fortune_card(BLANK_CARDS[1])
        self.window.blit(DICE.icon, DICE.rect)
        pygame.display.update()

    def display_gameover(self):
        self.window.fill(RED)
        # wish = pygame.transform.scale(pygame.image.load('img/wish.png'), (600, 400))
        # vic_screen1 = pygame.transform.scale(pygame.image.load('img/thelamp.jpg'), (WINWIDTH, WINHEIGHT))
        # vic_screen2 = pygame.transform.scale(pygame.image.load('img/genie.jpg'), (WINWIDTH, WINHEIGHT))
        # info_surf = TITLEFONT.render('ANYONE HERE?? press SPACE to get me out!!!', True, AMBER)
        # info_rect = info_surf.get_rect()
        # info_rect.topleft = (WINWIDTH / 2) - (info_surf.get_width() / 2), (WINHEIGHT - 50)
        # cont = True
        # while cont:
        #     checkForQuit()
        #     WIN.blit(vic_screen1, (0, 0))
        #     WIN.blit(info_surf, info_rect)
        #     pygame.display.update()
        #     for event in pygame.event.get():
        #         if event.type == pygame.KEYUP:
        #             if event.key == pygame.K_SPACE:
        #                 cont = False
        # while True:
        #     checkForQuit()
        #     WIN.blit(vic_screen2, (0, 0))
        #     vic_surf = TITLEFONT.render('YOU FOUND ME!!!', True, AMBER)
        #     vic_rect = vic_surf.get_rect()
        #     vic_rect.topleft = (WINWIDTH / 2) - (vic_surf.get_width() / 2), WINHEIGHT - 50
        #     WIN.blit(vic_surf, vic_rect)
        #     pygame.display.update()
        #     for event in pygame.event.get():
        #         if event.type == pygame.KEYUP:
        #             if event.key == pygame.K_SPACE:
        #                 WIN.blit(vic_screen2, (0, 0))
        #                 WIN.blit(wish, (5, 20))
        #                 pygame.display.update()
        #                 while True:
        #                     for event in pygame.event.get():
        #                         if event.type == pygame.KEYUP:
        #                             if event.key == pygame.K_n:
        #                                 mainMenu()
        #                             if event.key == pygame.K_q:
        #                                 terminate()

    def updateScreen(self, board, player):
        pass
        # self.drawBoard(main_board, dice_num)
        # movePlayer(main_board, player1.tile, player1.img)
        # movePlayer(main_board, player2.tile, player2.img)
        # WIN.blit(player1.img, (INFO1_X + 10, INFO1_Y + 10))
        # WIN.blit(player2.img, (INFO2_X + 10, INFO2_Y + 10))
        # if player == player1:
        #     WIN.blit(player1.logo, (TURNX, TURNY))
        #     WIN.blit(player2.logo, (-1000, TURNY))
        #     pygame.draw.rect(WIN, ORANGE, (INFO1_X + 10, INFO1_Y + 10, 70, 70))
        # if player == player2:
        #     WIN.blit(player2.logo, (TURNX, TURNY))
        #     WIN.blit(player1.logo, (-1000, TURNY))
        #     pygame.draw.rect(WIN, ORANGE, (INFO2_X + 10, INFO2_Y + 10, 70, 70))
        # WIN.blit(player1.img, (INFO1_X + 10, INFO1_Y + 10))
        # WIN.blit(player2.img, (INFO2_X + 10, INFO2_Y + 10))
        # player1.showItem()
        # player1.healthBar()
        # player2.showItem()
        # player2.healthBar()
        # pygame.display.update()
