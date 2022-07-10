import random

class Player:
    LOGO_SIZE = 128, 128

    def __init__(self, turn):
        self.id = turn
        self.max_health = 100
        self.health = 100
        self._tile = 1
        self._items = []
        self.hero = 'None'
        self.sprite = None

    @property
    def tile(self):
        return self._tile

    @property
    def hero_name(self):
        return self.hero

    @property
    def inventory(self) -> list:
        return self._items

    def set_hero(self, hero, sprite):
        self.hero = hero
        self.sprite = sprite

    def add_item(self, item):
        if item not in self._items:
            self._items.append(item)

    def use_item(self, item):
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def has_item(self, item):
        if item in self._items:
            return True
        return False

    def move_to(self, square):
        self._tile = square

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health < 0:
            self.health = 0

    def heal(self, hp):
        self.health += hp
        if self.health > self.max_health:
            self.health = self.max_health

    @property
    def luck(self):
        return random.randint(1, 5)

    def attack_monster(self, dmg, stk):
        if self.has_item('SPCL'):
            self.use_item('SPCL')
        else:
            if self.has_item('ATK'):
                self.use_item('ATK')
            else:
                self.tile -= stk
                if self.tile < 1:
                    self.tile = 1
            if self.has_item('DEF'):
                self.use_item('DEF')
            else:
                self.health -= dmg
                if self.health <= 0:
                    self.health = 100
                    self.tile = 1
