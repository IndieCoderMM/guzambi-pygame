import random
from .constants import BOARD_SIZE, BACKS, ITEMS, POTIONS, Dragons, BEASTS, CardType
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
        self._chosen_card = None
        self.current_card_img = BACKS.img

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
    def roll_dice():
        return random.choice(range(1, 5))

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

    def get_fortune_card(self):
        self._chosen_card = self._fortune_card
        self.current_card_img = self._chosen_card.img

    def take_action(self):
        card = self._chosen_card
        if card.type == CardType.HEAL:
            self.current_player.heal(card.ability)
        elif card.type == CardType.SPEED:
            self.move_player(card.ability)
        elif card.type == CardType.DRAGON or card.type == CardType.BEAST:
            self.current_player.attack_monster(card.dmg, card.step)
        else:
            self.current_player.add_item(card)
        self.current_card_img = BACKS.img
        self.next_turn()

    @property
    def _fortune_card(self):
        luck_meter = self.current_player.luck
        if luck_meter <= 2:
            monster_level = self.current_player.luck
            if monster_level == 5:
                print('Dragon', monster_level, luck_meter)
                return Dragons
            else:
                print('Monster', monster_level, luck_meter)
                return BEASTS
        elif luck_meter <= 4:
            print('Item')
            return random.choice(ITEMS)
        else:
            print('Potion')
            return random.choice(POTIONS)

