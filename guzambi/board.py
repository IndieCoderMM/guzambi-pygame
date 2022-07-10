import random
from .constants import BOARD_SIZE, ITEMS, POTIONS, DRAGON, BEAST
from .player import Player

class Board:
    ROWS = BOARD_SIZE
    COLS = BOARD_SIZE
    SIZE = BOARD_SIZE * BOARD_SIZE

    def __init__(self):
        self.table = self.get_table()
        self.p1 = Player('P1')
        self.p2 = Player('P2')
        self.current_player = self.p1

    def get_table(self):
        table = []
        for r in range(self.ROWS):
            row = []
            for c in range(self.COLS):
                tile = self.SIZE - c - self.ROWS * r
                row.append(tile)
            table.append(row)
        for i, r in enumerate(table):
            if (i % 2 == 0 and self.SIZE % 2 != 0) or (i % 2 != 0 and self.SIZE % 2 == 0):
                r.reverse()
        return table

    def tile(self, row, col):
        return self.table[row][col]

    @property
    def winner(self):
        if self.p1.tile == self.SIZE:
            return self.p1
        elif self.p2.tile == self.SIZE:
            return self.p2

    @staticmethod
    def roll_dice(from_, to_):
        return random.choice(range(from_, to_ + 1))

    def set_hero(self, hero):
        if self.p1.sprite is None:
            self.p1.set_hero(hero.name, hero.sprite)
            return False
        self.p2.set_hero(hero.name, hero.sprite)
        return True

    def next_turn(self):
        self.current_player = self.p2 if self.current_player == self.p1 else self.p1

    def move_player(self, step):
        square = self.current_player.tile + step
        if square >= self.SIZE:
            square = self.SIZE
        self.current_player.move_to(square)
        self.next_turn()

    def get_fortune_card(self):
        player = self.current_player
        luck_meter = player.luck
        if luck_meter <= 2:
            monster_level = player.luck
            if monster_level == 5:
                print('Dragon', monster_level, luck_meter)
                return DRAGON
            else:
                print('Monster', monster_level, luck_meter)
                return BEAST
        elif luck_meter <= 4:
            print('Item')
            return random.choice(ITEMS)
        else:
            print('Potion')
            return random.choice(POTIONS)
