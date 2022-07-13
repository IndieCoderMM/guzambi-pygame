import random
from .constants import Item, CardType, Image

class Player:
    LOGO_SIZE = 128, 128

    def __init__(self, turn: str, max_health: int = 100):
        self.id = turn
        self.max_health = max_health
        self.health = max_health
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
    def inventory(self) -> list[Item]:
        return self._items

    def set_hero(self, hero: str, sprite: Image):
        self.hero = hero
        self.sprite = sprite

    def add_item(self, item: Item):
        if item not in self._items:
            self._items.append(item)
            print(f"*Collected [ {item} ] to inventory*")

    def use_item(self, itype: CardType):
        for item in self._items:
            if item.type == itype:
                self._items.remove(item)
                print(f"*Used [ {item} ] from inventory*")
                return True
        return False

    def has_item(self, itype: CardType):
        for item in self._items:
            if item.type == itype:
                return True
        return False

    def move_to(self, square: int):
        self._tile = square

    def retreat(self, step: int):
        self._tile -= step
        if self._tile < 1:
            self._tile = 1

    def take_damage(self, dmg: int):
        self.health -= dmg
        if self.health < 0:
            self.health = 0

    def heal(self, hp: int):
        self.health += hp
        if self.health > self.max_health:
            self.health = self.max_health

    @staticmethod
    def luck(from_: int, to_: int):
        return random.randint(from_, to_)

    def attack_monster(self, dmg: int, step: int):
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
