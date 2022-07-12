from .constants import WIDTH, HEIGHT, MARGIN, TILE_WIDTH, HEADER, LEGENDS, DICE, BOARD_WIDTH, FOOTER, CardType, COVER_IMG, GLASS, RED, LIGHT, BLUE, DARK, GREEN, YELLOW, GREY, ORANGE, PURPLE, NAMEPAD, NAMEPAD_ACTIVE, ICONPAD, WINNER_BADGE, MSGPAD
from .player import Player
from .board import Board
import pygame

Image = pygame.Surface

class GUI:
    TILE_COLOR = GLASS
    BORDER_COLOR = ORANGE
    DEFAULT_FONT = 'poorrichard'
    TITLE_FONT = 'rockwellextra'
    BG_COLOR = BLUE

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
    def get_selected_hero(pos: tuple):
        x, y = pos
        for hero in LEGENDS:
            if hero.card_rect.collidepoint(x, y):
                return hero
        return None

    @staticmethod
    def dice_clicked(pos: tuple):
        x, y = pos
        if DICE.rect.collidepoint(x, y):
            return True
        return False

    def draw_text(self, txt: str, color: tuple, size: int, x: int = 0, y: int = 0, align: str = 'None', title: bool = False, shadow: bool = False, bg_img: Image = None):
        font_fam = self.TITLE_FONT if title else self.DEFAULT_FONT
        font = pygame.font.SysFont(font_fam, size)
        text = font.render(txt, True, color)
        if align == 'center':
            x = WIDTH // 2 - text.get_width() // 2
        elif align == 'right':
            x = WIDTH - text.get_width() - MARGIN
        elif align == 'left':
            x = MARGIN
        if shadow:
            shadow_text = font.render(txt, True, GREY)
            offset = size // 15
            self.window.blit(shadow_text, (x+offset, y+offset))
        if bg_img:
            resized = pygame.transform.scale(bg_img, (text.get_width()+40, text.get_height()+20))
            self.window.blit(resized, (x-20, y-10))
        self.window.blit(text, (x, y))

    def draw_health_bar(self, player: Player, x: int, y: int, length: int, thickness: int = 20):
        pygame.draw.rect(self.window, DARK, (x-2, y-2, length+4, thickness+4))
        pygame.draw.rect(self.window, RED, (x, y, length, thickness))
        bar_length = length * player.health // player.max_health
        if player.id == 'P2':
            x += length - bar_length
        health_color = GREEN if player.health > player.max_health // 2 else YELLOW
        pygame.draw.rect(self.window, health_color, (x, y, bar_length, thickness))

    def show_status(self, p1: Player, p2: Player, turn: Player):
        if turn == p1:
            p1_bg = NAMEPAD_ACTIVE
            p2_bg = NAMEPAD
        else:
            p1_bg = NAMEPAD
            p2_bg = NAMEPAD_ACTIVE
        self.draw_text(p1.hero_name, DARK, 20, y=10, align='left', bg_img=p1_bg)
        self.draw_text(p2.hero_name, DARK, 20, y=10, align='right', bg_img=p2_bg)
        bar_length = 150
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
            pygame.draw.rect(self.window, YELLOW, (x-2, y-2, item.icon.get_width()+4, item.icon.get_width()+4))
            self.window.blit(item.icon, (x, y))

    def draw_tile(self, num: int, row: int, col: int):
        left, top = self.get_left_top(col, row)
        # pygame.draw.rect(self.window, WHITE, (left, top, TILE_WIDTH, TILE_WIDTH))
        t = pygame.Surface((TILE_WIDTH, TILE_WIDTH), pygame.SRCALPHA)
        t.fill(self.TILE_COLOR)
        self.window.blit(t, (left, top))
        textx = left + int(TILE_WIDTH / 2)
        texty = top + int(TILE_WIDTH / 2)
        self.draw_text(str(num), DARK, 20, textx, texty)

    def show_dice_num(self, num):
        dice_img = DICE.get_num_img(num)
        x = DICE.rect.x - DICE.rect.width - 10
        y = DICE.rect.y
        self.window.blit(ICONPAD, (x-5, y-4))
        self.window.blit(dice_img, (x, y))
        pygame.display.update()

    def draw_dice_animation(self, board):
        for _ in range(20):
            num = board.roll_dice()
            self.show_dice_num(num)
            pygame.time.wait(100)

    def draw_board(self, board: Board):
        left, top = self.get_left_top(0, 0)
        # pygame.draw.rect(self.window, GREEN, (left, top, BOARD_WIDTH, BOARD_WIDTH))
        for row in range(board.ROWS):
            for col in range(board.COLS):
                self.draw_tile(board.tile(row, col), row, col)
        pygame.draw.rect(self.window, self.BORDER_COLOR, (left - 5, top - 5, BOARD_WIDTH + 12, BOARD_WIDTH + 12), 4)

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

    def draw_card(self, card_img: Image, rect: pygame.Rect, pos: tuple[int, int]):
        rect.topleft = pos
        self.window.blit(card_img, pos)

    def draw_selection_cards(self, board: Board):
        for i, hero in enumerate(LEGENDS):
            y = HEIGHT - FOOTER - hero.card_rect.height
            gap = ((WIDTH - MARGIN * 2) - hero.card_rect.width * len(LEGENDS)) // (len(LEGENDS)+1)
            x = MARGIN + hero.card_rect.width * i + gap * (i+1)
            self.draw_card(hero.card, hero.card_rect, (x, y))
            if hero.sprite == board.p1.sprite:
                self.draw_text('P1', YELLOW, 20, x+hero.card_rect.width//2, y-20, title=True)
            elif hero.sprite == board.p2.sprite:
                self.draw_text('P2', YELLOW, 20, x+hero.card_rect.width//2, y-20, title=True)

    def display_info(self, txt):
        self.draw_text(txt, YELLOW, 20, y=HEADER-50, align='center', bg_img=MSGPAD)
        pygame.display.update()

    def display_menu(self, board):
        self.window.fill(self.BG_COLOR)
        self.draw_text('GUZAMBI', YELLOW, 70, align='center', title=True, shadow=True)
        self.draw_text('Journey Into Mystery', ORANGE, 30, y=80, align='center', title=True, shadow=True)
        if board.p1.sprite is None:
            selecting_player = 'Player 1'
        else:
            selecting_player = 'Player 2'
        self.draw_selection_cards(board)
        if board.p2.sprite is not None:
            self.draw_text(f'Entering into the Valley of Death...', LIGHT, 30, y=HEADER + 30, align='center', shadow=True)
            pygame.display.update()
            pygame.time.wait(500)
        else:
            self.draw_text(f'[ {selecting_player} ] Select Your Hero...', LIGHT, 30, y=HEADER + 30, align='left', shadow=True)
        pygame.display.update()

    def display_fortune_card(self, card_img: Image):
        x = WIDTH - MARGIN - card_img.get_width() * 1.5
        y = HEADER
        self.draw_card(card_img, card_img.get_rect(), (x, y))
        pygame.display.update()

    def display_game(self, board: Board):
        self.window.blit(COVER_IMG, (0, 0))
        self.draw_board(board)
        self.draw_player(board)
        self.show_status(board.p1, board.p2, board.current_player)
        self.display_fortune_card(board.current_card_img)
        self.window.blit(ICONPAD, (DICE.rect.x-5, DICE.rect.y-4))
        self.window.blit(DICE.icon, DICE.rect)
        pygame.display.update()

    def display_gameover(self, board):
        self.window.blit(COVER_IMG, (0, 0))
        self.window.blit(WINNER_BADGE, (WIDTH//2-WINNER_BADGE.get_width()//2, 30))
        self.draw_text(f"{board.winner.hero_name}", ORANGE, 20, y=HEIGHT//2-80, align='center', title=True)
        self.draw_text("has completed the journey!", GREY, 25, y=HEIGHT // 2 - 50, align='center')
        self.draw_text("Another adventures", GREY, 20, y=HEIGHT//2, align='center')
        self.draw_text(" are waiting for you...", GREY, 20, y=HEIGHT // 2 + 35, align='center')

        pygame.display.update()

