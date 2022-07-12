import random
from .constants import Item, CardType

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

    def add_item(self, item: Item):
        if item not in self._items:
            self._items.append(item)
            print(f"*Collected [ {item} ] to inventory*")

    def use_item(self, itype):
        for item in self._items:
            if item.type == itype:
                self._items.remove(item)
                print(f"*Used [ {item} ] from inventory*")
                return True
        return False

    def has_item(self, itype):
        for item in self._items:
            if item.type == itype:
                return True
        return False

    def move_to(self, square):
        self._tile = square

    def retreat(self, step):
        self._tile -= step
        if self._tile < 1:
            self._tile = 1

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

    def attack_monster(self, dmg, step):
        if self.has_item(CardType.MAGIC):
            self.use_item(CardType.MAGIC)
            print('*Defeated monster with the power of Magic*')
        else:
            if self.has_item(CardType.DEFEND):
                self.use_item(CardType.MAGIC)
                print('*Blocked damage from monster*')
            else:
                self.take_damage(dmg)
                print(f'$Took [ {dmg} ] damage from the monster$')
            if self.has_item(CardType.ATTACK):
                self.use_item(CardType.ATTACK)
                print('*Slayed monster to death*')
            else:
                self.retreat(step)
                print(f'$Not enough weapon! Retreated [ {step} ] steps for recovery$')

        # def attack_monster(self, dmg, stk):
    #     if self.has_item('SPCL'):
    #         self.use_item('SPCL')
    #     else:
    #         if self.has_item('ATK'):
    #             self.use_item('ATK')
    #         else:
    #             self.tile -= stk
    #             if self.tile < 1:
    #                 self.tile = 1
    #         if self.has_item('DEF'):
    #             self.use_item('DEF')
    #         else:
    #             self.health -= dmg
    #             if self.health <= 0:
    #                 self.health = 100
    #                 self.tile = 1
